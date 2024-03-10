import config_loader

configs = config_loader.ConfigLoader()


def save_start_page_token(token):
    with open('drive_start_page_token.txt', 'w') as file:
        file.write(token)

def load_start_page_token(service):
    try:
        with open('drive_start_page_token.txt', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        response = service.changes().getStartPageToken().execute()
        start_page_token = response.get('startPageToken')
        save_start_page_token(start_page_token)
        return start_page_token

def get_changes(service, start_page_token):
    changes = []
    page_token = start_page_token
    while page_token is not None:
        response = service.changes().list(pageToken=page_token, spaces='drive',
                                          fields="nextPageToken, newStartPageToken, changes(removed, fileId, file(id, name, mimeType, webViewLink, size, createdTime, modifiedTime))").execute()
        changes.extend(response.get('changes', []))
        if 'newStartPageToken' in response:
            save_start_page_token(response['newStartPageToken'])
        page_token = response.get('nextPageToken')
    return changes


def delete_from_notion(file_id, notion_client, NOTION_DATABASE_ID):
    try:
        notion_pages = notion_client.databases.query(
            database_id=NOTION_DATABASE_ID,
            filter={"property": "Drive File ID", "rich_text": {"equals": file_id}}
        )
        for page in notion_pages['results']:
            notion_client.pages.update(
                page['id'],
                archived=True
            )
    except Exception as e:
        print(f"Error removing from Notion: {e}")


def sync_to_notion(file, notion_client, NOTION_DATABASE_ID, removed=False):
    if removed:
        delete_from_notion(file['id'], notion_client, NOTION_DATABASE_ID)
        return
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
        print(change)
        if 'file' in change and not change.get('removed', False):
            sync_to_notion(change['file'], configs.notion_client, configs.NOTION_DATABASE_ID)
        elif change.get('removed', False):
            # Handle removed files
            sync_to_notion({'id': change['fileId']}, configs.notion_client, configs.NOTION_DATABASE_ID, removed=True)

if __name__ == '__main__':
    main()