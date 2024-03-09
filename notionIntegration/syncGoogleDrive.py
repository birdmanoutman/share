import json

from google.oauth2 import service_account
from googleapiclient.discovery import build
from notion_client import Client as NotionClient

# 读取配置
with open('../configs/notionIntConfig.json', 'r', encoding='utf-8') as file:
    CONFIGURATION = json.load(file)
    NOTION_DATABASE_ID = CONFIGURATION['DATABASE']['TXT']
    NOTION_TOKEN = CONFIGURATION["NOTION_TOKEN"]

SERVICE_ACCOUNT_FILE = r'C:\Users\dell\Desktop\share\configs\enzo-file-management-734d6e6d56da.json'

# Notion配置
notion_client = NotionClient(auth=NOTION_TOKEN)


# 获取Google Drive服务实例
def get_google_drive_service():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/drive'])
    service = build('drive', 'v3', credentials=credentials, cache_discovery=False, )
    return service


service = get_google_drive_service()


# 修改后的获取Google Drive指定文件夹的文件列表函数
def list_google_drive_files(folder_id):
    files = []
    query = f"'{folder_id}' in parents and trashed=false"
    page_token = None
    while True:
        results = service.files().list(q=query,
                                       pageSize=100,  # 增加pageSize以减少请求次数，但不超过1000
                                       fields="nextPageToken, files(id, name, mimeType, modifiedTime, webViewLink)",
                                       pageToken=page_token).execute()
        files.extend(results.get('files', []))
        page_token = results.get('nextPageToken', None)
        if page_token is None:
            break
    return files


# 创建或更新Notion数据库记录
def sync_to_notion(file, notion_client, NOTION_DATABASE_ID):
    try:
        # 尝试查询Notion数据库以查找匹配的Google Drive文件ID
        notion_pages = notion_client.databases.query(
            database_id=NOTION_DATABASE_ID,
            filter={
                "property": "Drive File ID",
                "rich_text": {
                    "equals": file['id']
                }
            }
        )

        # 根据查询结果决定是创建新页面还是更新现有页面
        if notion_pages['results']:
            page_id = notion_pages['results'][0]['id']
            notion_client.pages.update(
                page_id=page_id,
                properties={
                    "Name": {
                        "title": [
                            {
                                "text": {
                                    "content": file['name'],
                                }
                            }
                        ]
                    },
                    "Drive Link": {
                        "url": file['webViewLink']
                    },
                    # 可以根据需要添加或更新更多属性
                }
            )
        else:
            notion_client.pages.create(
                parent={"database_id": NOTION_DATABASE_ID},
                properties={
                    "Name": {
                        "title": [
                            {
                                "text": {
                                    "content": file['name'],
                                }
                            }
                        ]
                    },
                    "Drive File ID": {
                        "rich_text": [
                            {
                                "text": {
                                    "content": file['id'],
                                }
                            }
                        ]
                    },
                    "Drive Link": {
                        "url": file['webViewLink']
                    },
                    # 可以根据需要添加更多属性
                }
            )
    except Exception as e:
        print(f"Error syncing to Notion: {e}")


# 主同步函数
def main():
    folder_id = '1-7JaTelGwbTuQ0YCuYIj61ugdEGAXf1y'
    files = list_google_drive_files(folder_id)
    for google_file in files:
        print(google_file)
        sync_to_notion(google_file, notion_client, NOTION_DATABASE_ID)


if __name__ == '__main__':
    main()
