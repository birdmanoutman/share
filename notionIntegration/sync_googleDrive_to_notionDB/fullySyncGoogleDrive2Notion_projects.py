from google.oauth2 import service_account
from googleapiclient.discovery import build
from notion_client import Client as NotionClient

import config_loader as cfg_loader


class GoogleDriveNotionSync:
    def __init__(self, config_loader, notion_database_name='sprintProjects', google_root_folder_name='sprintProjects'):
        self.existing_notion_entries = None
        self.config_loader = config_loader
        self.notion_client = NotionClient(auth=self.config_loader.NOTION_TOKEN)
        self.google_service = self.get_google_drive_service()
        self.notion_database_id = self.config_loader.NOTION_DATABASE_IDs[notion_database_name]
        self.refresh_existing_notion_entries()
        self.google_root_folder_id = self.config_loader.GOOGLE_DRIVE_IDs[google_root_folder_name]

    def refresh_existing_notion_entries(self):
        """Refresh the list of existing Notion entries from the database."""
        self.existing_notion_entries = self.fetch_all_notion_entries()

    def get_google_drive_service(self):
        """Set up Google Drive service."""
        credentials = service_account.Credentials.from_service_account_file(
            self.config_loader.GOOGLE_SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/drive'])
        return build('drive', 'v3', credentials=credentials)

    def fetch_all_notion_entries(self):
        """Fetch all Notion entries with their Google Drive IDs."""
        notion_entries = {}
        start_cursor = None
        while True:
            try:
                response = self.notion_client.databases.query(database_id=self.notion_database_id,
                                                              start_cursor=start_cursor)
                for page in response.get('results', []):
                    drive_file_id_list = page['properties'].get('Google Drive ID', {}).get('rich_text', [])
                    if drive_file_id_list:
                        notion_entries[drive_file_id_list[0].get('plain_text')] = page['id']
                if not response.get('has_more', False):
                    break
                start_cursor = response.get('next_cursor')
            except Exception as e:
                print(f"Error fetching Notion entries: {e}")
                break
        return notion_entries

    def check_if_page_exists(self, google_drive_id):
        """Check if a Notion page for a given Google Drive ID exists."""
        exists = self.existing_notion_entries.get(google_drive_id)
        print(
            f"{'Found' if exists else 'No'} existing Notion page for Google Drive ID {google_drive_id}: {exists or ''}")
        return exists

    def list_drive_files(self, folder_id=None):
        """List files in a given Google Drive folder."""
        query = f"'{folder_id}' in parents" if folder_id else "'root' in parents"
        response = self.google_service.files().list(q=query, spaces='drive',
                                                    fields='nextPageToken, files(id, name, mimeType, parents)').execute()
        return response.get('files', [])

    def create_or_update_notion_page(self, file_info, parent_notion_id=None):
        """Create or update a Notion page based on Google Drive file info."""
        notion_page_id = self.check_if_page_exists(file_info['id'])
        properties = self.prepare_notion_page_properties(file_info, parent_notion_id)

        if notion_page_id:
            self.notion_client.pages.update(notion_page_id, properties=properties)
        else:
            page_data = {"parent": {"database_id": self.notion_database_id}, "properties": properties}
            response = self.notion_client.pages.create(**page_data)
            notion_page_id = response['id']
        return notion_page_id

    @staticmethod
    def prepare_notion_page_properties(file_info, parent_notion_id):
        """Prepare properties for a Notion page based on Google Drive file info."""
        is_folder = file_info['mimeType'] == 'application/vnd.google-apps.folder'
        properties = {
            "Name": {"title": [{"text": {"content": file_info['name']}}]},
            "Type": {"select": {"name": "Folder" if is_folder else "File"}},
            "Google Drive Link": {
                "url": f"https://drive.google.com/drive/folders/{file_info['id']}" if is_folder else f"https://drive.google.com/file/d/{file_info['id']}/view"
            },
            "Google Drive ID": {"rich_text": [{"text": {"content": file_info['id']}}]}
        }

        if parent_notion_id:
            properties["Parent"] = {"relation": [{"id": parent_notion_id}]}
        return properties

    def sync_folder(self, folder_id=None, parent_notion_id=None):
        """Sync a Google Drive folder to a Notion database."""
        drive_files = self.list_drive_files(folder_id)
        for file in drive_files:
            notion_id = self.create_or_update_notion_page(file, parent_notion_id)
            if file['mimeType'] == 'application/vnd.google-apps.folder':
                self.sync_folder(file['id'], notion_id)

    def run_sync(self):
        """Run the synchronization process."""
        self.refresh_existing_notion_entries()
        self.sync_folder(self.google_root_folder_id)
        self.delete_orphan_notion_pages()

    def delete_orphan_notion_pages(self):
        """Delete orphaned Notion pages that no longer have a corresponding file in Google Drive."""
        for drive_id, notion_id in self.existing_notion_entries.items():
            if not self.check_if_drive_file_exists(drive_id):
                self.notion_client.pages.update(notion_id, archived=True)

    def check_if_drive_file_exists(self, drive_id):
        """Check if a file exists in Google Drive."""
        try:
            self.google_service.files().get(fileId=drive_id).execute()
            return True
        except Exception as e:
            print(f"Error checking file existence: {e}")
            return False

    def remove_duplicates(self):
        """Identify and remove duplicate Notion pages based on Google Drive ID."""
        # Refresh the existing notion entries to ensure we're working with the latest data.
        self.refresh_existing_notion_entries()

        seen_ids = set()
        duplicates = []

        # Iterate through the existing Notion entries to find duplicates.
        for drive_id, notion_id in self.existing_notion_entries.items():
            if drive_id in seen_ids:
                duplicates.append(notion_id)
            else:
                seen_ids.add(drive_id)

        # Archive the duplicates in Notion.
        for notion_id in duplicates:
            try:
                self.notion_client.pages.update(notion_id, archived=True)
                print(f"Archived duplicate Notion page: {notion_id}")
            except Exception as e:
                print(f"Failed to archive Notion page: {notion_id}, Error: {e}")


if __name__ == "__main__":
    config_loader_instance = cfg_loader.ConfigLoader()
    sync_instance = GoogleDriveNotionSync(config_loader_instance)
    sync_instance.remove_duplicates()  # Optional: remove duplicates before syncing
    sync_instance.run_sync()
