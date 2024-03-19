from google.oauth2 import service_account
from googleapiclient.discovery import build
from notion_client import Client as NotionClient

import config_loader as cfg_loader


class GoogleDriveNotionSync:
    def __init__(self, config_loader):
        self.config_loader = config_loader
        self.notion_client = NotionClient(auth=self.config_loader.NOTION_TOKEN)
        self.google_service = self.get_google_drive_service()
        self.notion_database_id = self.config_loader.NOTION_DATABASE_IDs['sprintProjects']
        self.existing_notion_entries = self.fetch_all_notion_entries()

    def fetch_all_notion_pages_with_titles(self):
        """Fetch all pages within the Notion database along with their titles and creation times."""
        pages_with_titles = []
        start_cursor = None
        while True:
            try:
                response = self.notion_client.databases.query(
                    database_id=self.notion_database_id,
                    start_cursor=start_cursor
                )
                for page in response.get('results', []):
                    page_title = page['properties'].get('Name', {}).get('title', [{}])[0].get('plain_text', '')
                    created_time = page['created_time']  # Capture the creation time for sorting
                    pages_with_titles.append((page['id'], page_title, created_time))

                if not response.get('has_more', False):
                    break
                start_cursor = response.get('next_cursor')
            except Exception as e:
                print(f"Error fetching Notion pages: {e}")
                break

        return pages_with_titles

    def remove_duplicates(self):
        """Identify and remove duplicate pages based on their titles, preserving only the earliest created instance."""
        pages_with_titles = self.fetch_all_notion_pages_with_titles()
        seen_titles = {}
        for page_id, title, created_time in sorted(pages_with_titles, key=lambda x: x[2]):  # Sort by creation time
            if title in seen_titles:
                # If we've seen this title before, delete the current page as it's a duplicate
                try:
                    self.notion_client.pages.update(page_id, archived=True)
                    print(f"Archived duplicate page: {title} (ID: {page_id})")
                except Exception as e:
                    print(f"Failed to archive page: {title} (ID: {page_id}), Error: {e}")
            else:
                # If this title hasn't been seen, mark it as seen
                seen_titles[title] = page_id

    def fetch_all_notion_entries(self):
        notion_entries = {}
        start_cursor = None
        while True:
            try:
                response = self.notion_client.databases.query(
                    database_id=self.notion_database_id,
                    start_cursor=start_cursor
                )
                for page in response.get('results', []):
                    drive_file_id_list = page['properties'].get('Google Drive ID', {}).get('rich_text', [])
                    if drive_file_id_list:
                        drive_file_id = drive_file_id_list[0].get('plain_text')
                        notion_entries[drive_file_id] = page['id']

                if not response.get('has_more', False):
                    break
                start_cursor = response.get('next_cursor')
            except Exception as e:
                print(f"Error fetching Notion entries: {e}")
                break

        return notion_entries

    def check_if_page_exists(self, google_drive_id):
        exists = self.existing_notion_entries.get(google_drive_id, None)
        if exists:
            print(f"Found existing Notion page for Google Drive ID {google_drive_id}: {exists}")
        else:
            print(f"No existing Notion page found for Google Drive ID {google_drive_id}.")
        return exists

    def get_google_drive_service(self):
        credentials = service_account.Credentials.from_service_account_file(
            self.config_loader.GOOGLE_SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/drive'])
        service = build('drive', 'v3', credentials=credentials)
        return service

    def list_drive_files(self, folder_id=None):
        query = f"'{folder_id}' in parents" if folder_id else "'root' in parents"
        response = self.google_service.files().list(q=query, spaces='drive',
                                                    fields='nextPageToken, files(id, name, mimeType, parents)').execute()
        return response.get('files', [])

    def create_or_update_notion_page(self, file_info, parent_notion_id=None):
        # 假设你已经有了一个方法来检查页面是否存在，并获取其ID
        notion_page_id = self.check_if_page_exists(file_info['id'])

        properties = {
            "Name": {
                "title": [{"text": {"content": file_info['name']}}]
            },
            "Type": {
                "select": {
                    "name": "Folder" if file_info['mimeType'] == 'application/vnd.google-apps.folder' else "File"}
            },
            "Google Drive Link": {
                "url": f"https://drive.google.com/file/d/{file_info['id']}/view"
            },
            "Google Drive ID": {  # Ensure this matches the exact name of the property in your Notion database
                "rich_text": [{"text": {"content": file_info['id']}}]
            }
        }

        if parent_notion_id:
            properties["Parent"] = {"relation": [{"id": parent_notion_id}]}

        if notion_page_id:  # 如果页面已存在，则更新
            self.notion_client.pages.update(notion_page_id, properties=properties)
        else:  # 否则，创建新页面
            page_data = {
                "parent": {"database_id": self.notion_database_id},
                "properties": properties
            }
            response = self.notion_client.pages.create(**page_data)
            notion_page_id = response['id']

        return notion_page_id

    def sync_folder(self, folder_id=None, parent_notion_id=None):
        drive_files = self.list_drive_files(folder_id)
        for file in drive_files:
            notion_id = self.create_or_update_notion_page(file, parent_notion_id)
            if file['mimeType'] == 'application/vnd.google-apps.folder':
                self.sync_folder(file['id'], notion_id)

    def check_if_drive_file_exists(self, drive_id):
        try:
            # 尝试获取文件信息；如果文件存在，这个调用会成功
            self.google_service.files().get(fileId=drive_id).execute()
            return True
        except Exception as e:
            # 如果文件不存在，Google Drive API会抛出一个异常
            # 根据你的Google API客户端库，这里捕获的异常类型可能需要调整
            print(f"Error checking file existence: {e}")
            return False

    def delete_orphan_notion_pages(self):
        # Determine orphaned pages and delete or archive them
        for drive_id, notion_id in self.existing_notion_entries.items():
            if not self.check_if_drive_file_exists(drive_id):  # Pseudocode for checking existence in Drive
                self.notion_client.pages.update(notion_id, archived=True)

    def run_sync(self, folder_id=None):
        self.existing_notion_entries = self.fetch_all_notion_entries()  # Refresh existing entries
        self.sync_folder(folder_id)
        self.delete_orphan_notion_pages()


if __name__ == "__main__":
    config_loader_instance = cfg_loader.ConfigLoader()  # Use a distinct name for clarity
    sync_instance = GoogleDriveNotionSync(config_loader_instance)

    sync_instance.remove_duplicates()  # Cast the spell to remove duplicates
    sync_instance.run_sync(config_loader_instance.GOOGLEDRIVE_IDs['sprintProjects'])
