import utils

configs = utils.ConfigLoader()


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


def get_changes(service, start_page_token):
    changes = []
    page_token = start_page_token
    while page_token is not None:
        response = service.changes().list(pageToken=page_token, spaces='drive',
                                          fields="nextPageToken, newStartPageToken, changes(file(id, name, mimeType, webViewLink, size, createdTime, modifiedTime))").execute()
        changes.extend(response.get('changes', []))
        if 'newStartPageToken' in response:
            save_start_page_token(response['newStartPageToken'])
        page_token = response.get('nextPageToken')
    return changes


def sync_to_notion(file, notion_client, NOTION_DATABASE_ID):
    try:
        notion_pages = notion_client.databases.query(
            database_id=NOTION_DATABASE_ID,
            filter={"property": "Drive File ID", "rich_text": {"equals": file['id']}}
        )

        webViewLink = file.get('webViewLink', '链接不可用')
        fileSize = file.get('size', '未知大小')
        createdDate = file.get('createdTime', '未知创建时间')[:10]  # 取日期部分 YYYY-MM-DD
        modifiedDate = file.get('modifiedTime', '未知修改时间')[:10]  # 取日期部分 YYYY-MM-DD

        if notion_pages['results']:
            page_id = notion_pages['results'][0]['id']
            notion_client.pages.update(
                page_id=page_id,
                properties={
                    "Name": {"title": [{"text": {"content": file['name']}}]},
                    "Drive Link": {"url": webViewLink},
                    "Size": {"number": int(fileSize) if fileSize.isdigit() else None},
                    "Created Date": {"date": {"start": createdDate}},
                    "Modified Date": {"date": {"start": modifiedDate}},
                }
            )
        else:
            notion_client.pages.create(
                parent={"database_id": NOTION_DATABASE_ID},
                properties={
                    "Name": {"title": [{"text": {"content": file['name']}}]},
                    "Drive File ID": {"rich_text": [{"text": {"content": file['id']}}]},
                    "Drive Link": {"url": webViewLink},
                    "Size": {"number": int(fileSize) if fileSize.isdigit() else None},
                    "Created Date": {"date": {"start": createdDate}},
                    "Modified Date": {"date": {"start": modifiedDate}},
                }
            )
    except Exception as e:
        print(f"Error syncing to Notion: {e}")


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
