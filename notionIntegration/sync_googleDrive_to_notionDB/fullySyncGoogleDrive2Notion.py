from concurrent.futures import ThreadPoolExecutor, as_completed

import config_loader

configs = config_loader.ConfigLoader()

# 获取Google Drive指定文件夹的文件列表函数
def list_google_drive_files(folder_id):
    files = []
    query = f"'{folder_id}' in parents and trashed=false"
    page_token = None
    while True:
        try:
            results = configs.google_service.files().list(
                q=query,
                pageSize=100,
                fields="nextPageToken, files(id, name, mimeType, modifiedTime, webViewLink, size, createdTime)",
                pageToken=page_token
            ).execute()

            files.extend(results.get('files', []))
            page_token = results.get('nextPageToken', None)
            if page_token is None:
                break
        except Exception as e:
            print(f"Error listing Google Drive files: {e}")
            break
    return files


def fetch_all_notion_entries(notion_client, notion_database_id):
    notion_entries = {}
    start_cursor = None
    while True:
        try:
            response = notion_client.databases.query(
                database_id=notion_database_id,
                start_cursor=start_cursor
            )
            for page in response.get('results', []):
                # 假设Drive File ID是作为富文本属性存储
                drive_file_id_list = page['properties'].get('Drive File ID', {}).get('rich_text', [])
                if drive_file_id_list:  # 确保列表不为空
                    drive_file_id = drive_file_id_list[0].get('plain_text')
                    notion_entries[drive_file_id] = page['id']

            if not response.get('has_more', False):
                break
            start_cursor = response.get('next_cursor')
        except Exception as e:
            print(f"Error fetching Notion entries: {e}")
            break

    return notion_entries


def sync_to_notion(google_file, notion_client, notion_database_id):
    try:
        # 尝试查询Notion数据库以查找匹配的Google Drive文件ID
        notion_pages = notion_client.databases.query(
            database_id=notion_database_id,
            filter={
                "property": "Drive File ID",
                "rich_text": {
                    "equals": google_file['id']
                }
            }
        ).get("results")

        webViewLink = google_file.get('webViewLink', '链接不可用')
        fileSize = int(google_file.get('size', 0))  # 假设文件大小存在且为整数
        createdTime = google_file['createdTime']  # 假设Google API总是返回这个字段
        modifiedTime = google_file['modifiedTime']  # 同上

        # Notion API的日期格式处理（需要调整为Notion接受的格式）
        created_date = {"start": createdTime.split('T')[0]}  # 只取日期部分
        modified_date = {"start": modifiedTime.split('T')[0]}  # 同上

        if notion_pages:
            page_id = notion_pages[0]['id']
            notion_client.pages.update(
                page_id=page_id,
                properties={
                    "Name": {"title": [{"text": {"content": google_file['name']}}]},
                    "Drive Link": {"url": webViewLink},
                    "Size": {"number": fileSize},
                    "Created Date": {"date": created_date},
                    "Modified Date": {"date": modified_date},
                }
            )
        else:
            notion_client.pages.create(
                parent={"database_id": notion_database_id},
                properties={
                    "Name": {"title": [{"text": {"content": google_file['name']}}]},
                    "Drive File ID": {"rich_text": [{"text": {"content": google_file['id']}}]},
                    # 这个是直接用来识别notion数据库中没有对应文件的
                    "Drive Link": {"url": webViewLink},
                    "Size": {"number": fileSize},
                    "Created Date": {"date": created_date},
                    "Modified Date": {"date": modified_date},
                }
            )
    except Exception as e:
        print(f"Error syncing to Notion: {e}")


def main():
    folder_id = configs.GOOGLEDRIVE_ID['TXT']
    files = list_google_drive_files(folder_id)
    notion_entries = fetch_all_notion_entries(configs.notion_client, configs.NOTION_DATABASE_ID)

    google_file_ids = {file['id']: file for file in files}  # Dictionary of Google Drive file ID to file object

    # 用于记录需要更新的文件ID
    files_to_update = {}

    # 检查Notion中哪些条目需要被删除或更新
    for drive_file_id, notion_page_id in notion_entries.items():
        if drive_file_id not in google_file_ids:
            # 删除不存在的文件对应的Notion条目
            try:
                configs.notion_client.pages.update(page_id=notion_page_id, archived=True)
                print(f"Archived Notion entry for missing Google Drive file ID: {drive_file_id}")
            except Exception as e:
                print(f"Error archiving Notion entry: {e}")
        else:
            # 标记存在的文件，稍后更新
            files_to_update[drive_file_id] = google_file_ids[drive_file_id]
            print("标记存在的文件，稍后更新:", drive_file_id)

    print("files to update:", files_to_update)
    # 更新或创建Notion条目
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_file = {executor.submit(sync_to_notion, file, configs.notion_client, configs.NOTION_DATABASE_ID): file
                          for file in google_file_ids.values()}
        for future in as_completed(future_to_file):
            file = future_to_file[future]
            try:
                future.result()  # 如果函数抛出异常，这里会重新抛出
                print(f"File {file['name']} synced successfully.")
            except Exception as e:
                print(f"Error syncing file {file['name']}: {e}")


if __name__ == '__main__':
    main()
