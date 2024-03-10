# 根据文件删除日期还原文件，但是由于服务账号（service account）的权限问题，似乎不起作用
import os
from datetime import datetime, timezone

from google.oauth2 import service_account
from googleapiclient.discovery import build

# 设置代理
os.environ['HTTP_PROXY'] = 'http://localhost:7890'
os.environ['HTTPS_PROXY'] = 'http://localhost:7890'

# 定义权限范围
SCOPES = ['https://www.googleapis.com/auth/drive']



# 获取Google Drive服务实例
def get_google_drive_service_viaServiceCount():
    # 服务账户文件位置
    SERVICE_ACCOUNT_FILE = '../../configs/enzo-file-management-734d6e6d56da.json'
    credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('drive', 'v3', credentials=credentials, cache_discovery=False)

# 还原文件函数
def restore_files(service):
    # 指定时间后的文件查询和还原
    time_after = datetime(2024, 3, 3, 13, 0, tzinfo=timezone.utc)
    results = service.files().list(q="trashed=True", fields='nextPageToken, files(id, name, trashedTime)').execute()
    print(results)
    for item in results.get('files', []):
        trashed_time = datetime.strptime(item['trashedTime'], '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc)
        if trashed_time > time_after:
            print(f"还原文件: {item['name']} ({item['id']})")
            service.files().update(fileId=item['id'], body={'trashed': False}).execute()

if __name__ == '__main__':
    service = get_google_drive_service_viaServiceCount()
    restore_files(service)
