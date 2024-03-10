import utils

configs = utils.ConfigLoader()

def get_changes(service, start_page_token):
    changes = []
    page_token = start_page_token
    while page_token is not None:
        response = service.changes().list(pageToken=page_token, spaces='drive', fields='nextPageToken, newStartPageToken, changes(fileId, file(name, id, mimeType, trashed, webViewLink))').execute()
        changes.extend(response.get('changes', []))
        if 'newStartPageToken' in response:
            # 更新你的存储的start_page_token为下次使用
            save_start_page_token(response['newStartPageToken'])
        page_token = response.get('nextPageToken')
    return changes

def sync_to_notion(file, notion_client, NOTION_DATABASE_ID):
    try:
        # 如果文件被标记为删除（即，移动到了回收站）
        if file.get('trashed', False):
            # 查询Notion数据库以找到匹配的记录，然后删除或标记为删除
            notion_pages = notion_client.databases.query(
                database_id=NOTION_DATABASE_ID,
                filter={
                    "property": "Drive File ID",
                    "rich_text": {
                        "equals": file['id']
                    }
                }
            )
            for page in notion_pages['results']:
                notion_client.pages.update(page_id=page['id'], archived=True)  # 标记为删除
            return

        # 检查是否存在webViewLink，如果不存在则设置为默认值
        webViewLink = file.get('webViewLink', '链接不可用')

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
                        "url": webViewLink
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
                        "url": webViewLink
                    },
                    # 可以根据需要添加更多属性
                }
            )
    except Exception as e:
        print(f"Error syncing to Notion: {e}")

def save_start_page_token(token):
    with open('drive_start_page_token.txt', 'w') as file:
        file.write(token)

def load_start_page_token(service):
    try:
        with open('drive_start_page_token.txt', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        # 如果文件不存在，获取新的start_page_token
        response = service.changes().getStartPageToken().execute()
        start_page_token = response.get('startPageToken')
        # 保存新获取的start_page_token以备后用
        save_start_page_token(start_page_token)
        return start_page_token

def main():
    service = configs.google_service
    start_page_token = load_start_page_token(service)
    changes = get_changes(service, start_page_token)
    for change in changes:
        if 'file' in change:
            google_file = change['file']
            sync_to_notion(google_file, configs.notion_client, configs.NOTION_DATABASE_ID)

if __name__ == '__main__':
    main()
