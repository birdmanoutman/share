import concurrent.futures
import logging

from google.oauth2 import service_account
from googleapiclient.discovery import build
from notion_client import Client as NotionClient

import config_loader as cfg_loader

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class GoogleDriveNotionSync:
    def __init__(self, config_loader, notion_database_name='sprintProjects', google_root_folder_name='sprintProjects'):
        self.config_loader = config_loader
        self.notion_client = NotionClient(auth=self.config_loader.NOTION_TOKEN)
        self.google_service = self.setup_google_drive_service()
        self.notion_database_id = self.config_loader.NOTION_DATABASE_IDs[notion_database_name]
        self.google_root_folder_id = self.config_loader.GOOGLE_DRIVE_IDs[google_root_folder_name]
        self.existing_notion_entries = self.fetch_all_notion_entries()

    def setup_google_drive_service(self):
        """Create the Google Drive service using credentials."""
        try:
            credentials = service_account.Credentials.from_service_account_file(
                self.config_loader.GOOGLE_SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/drive'])
            return build('drive', 'v3', credentials=credentials)
        except Exception as e:
            print(f"Failed to set up Google Drive service: {e}")
            raise

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

    def list_drive_files(self, folder_id=None):
        """List files in a Google Drive folder."""
        query = f"'{folder_id}' in parents" if folder_id else "'root' in parents"
        try:
            response = self.google_service.files().list(q=query, spaces='drive',
                                                        fields='nextPageToken, files(id, name, mimeType, parents)').execute()
            return response.get('files', [])
        except Exception as e:
            print(f"Failed to list Google Drive files: {e}")
            raise

    def create_or_update_notion_page(self, file_info, parent_notion_id=None):
        """Create or update a Notion page."""
        notion_page_id = self.existing_notion_entries.get(file_info['id'])
        properties = self.prepare_notion_page_properties(file_info, parent_notion_id)

        try:
            if notion_page_id:
                self.notion_client.pages.update(page_id=notion_page_id, properties=properties)
                print(f"update:{notion_page_id}")
            else:
                page_data = {"parent": {"database_id": self.notion_database_id}, "properties": properties}
                response = self.notion_client.pages.create(**page_data)
                notion_page_id = response['id']
                print(f"create:{notion_page_id}")
        except Exception as e:
            print(f"Failed to create or update Notion page: {e}")
            raise
        return notion_page_id

    @staticmethod
    def prepare_notion_page_properties(file_info, parent_notion_id):
        """Prepare properties for a Notion page."""
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
        """Sync Google Drive folder with Notion using concurrency."""
        drive_files = self.list_drive_files(folder_id)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_file = {executor.submit(self.create_or_update_notion_page, file, parent_notion_id): file for file
                              in drive_files}
            for future in concurrent.futures.as_completed(future_to_file):
                file = future_to_file[future]
                try:
                    notion_id = future.result()
                    if file['mimeType'] == 'application/vnd.google-apps.folder':
                        self.sync_folder(file['id'], notion_id)
                except Exception as e:
                    logger.error("Failed to sync file %s: %s", file['name'], e, exc_info=True)

    def run_sync(self):
        """Main method to run the sync process."""
        self.sync_folder(self.google_root_folder_id)


if __name__ == "__main__":
    config_loader_instance = cfg_loader.ConfigLoader()
    sync_instance = GoogleDriveNotionSync(config_loader_instance)
    sync_instance.run_sync()
