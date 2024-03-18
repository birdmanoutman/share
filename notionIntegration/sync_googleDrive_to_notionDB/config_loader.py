import json
import os

from google.oauth2 import service_account
from googleapiclient.discovery import build
from notion_client import Client as NotionClient


class ConfigLoader:
    def __init__(self, config_path='../../configs'):
        # 通过环境变量设置代理，以便于管理和更改，避免硬编码
        self.setup_proxy()

        # 使用绝对路径加载配置文件，增加代码的可移植性
        notion_config_path = os.path.join(config_path, 'notionIntConfig.json')
        google_config_path = os.path.join(config_path, 'enzo-file-management-734d6e6d56da.json')

        self.load_notion_config(notion_config_path)
        self.GOOGLE_SERVICE_ACCOUNT_FILE = google_config_path

        # 初始化Notion和Google Drive服务
        self.notion_client = NotionClient(auth=self.NOTION_TOKEN)
        self.google_service = self.get_google_drive_service()

    @staticmethod
    def setup_proxy():
        proxy = os.getenv('PROXY_URL', 'http://localhost:7890')  # 从环境变量读取，如果不存在则使用默认值
        os.environ['HTTP_PROXY'] = proxy
        os.environ['HTTPS_PROXY'] = proxy
        # os.environ['PYTHONHTTPSVERIFY'] = '0'  # 设置环境变量PYTHONHTTPSVERIFY=0来禁用HTTPS验证作为临时的解决方法。

    def load_notion_config(self, config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                configuration = json.load(file)
                self.NOTION_DATABASE_IDs = configuration['DATABASE']
                self.NOTION_TOKEN = configuration["NOTION_TOKEN"]
                self.GOOGLEDRIVE_IDs = configuration["GOOGLEDRIVE_ID"]
        except FileNotFoundError:
            print("Notion configuration file not found.")
            raise
        except json.JSONDecodeError:
            print("Error decoding Notion configuration file.")
            raise

    def get_google_drive_service(self):
        try:
            credentials = service_account.Credentials.from_service_account_file(
                self.GOOGLE_SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/drive'])
            service = build('drive', 'v3', credentials=credentials, cache_discovery=False)
            return service
        except Exception as e:
            print(f"Failed to initialize Google Drive service: {e}")
            raise


# 使用示例
if __name__ == '__main__':
    config_loader = ConfigLoader()
    # 这里可以添加其他用途，例如使用config_loader.notion_client或config_loader.google_service进行操作
