import concurrent.futures
import json
import os
from notion_client import Client

with open(r'../configs/notionIntConfig.json', 'r', encoding='utf-8') as file:
    configdata = json.load(file)

# Notion配置
DATABASE_ID = configdata['DATABASE']['sprintProjects']
NOTION_TOKEN = configdata['NOTION_TOKEN']

# 初始化Notion客户端
notion = Client(auth=NOTION_TOKEN)


def create_page(database_id, path, parent_path=None, is_folder=False):
    """在Notion数据库中创建一个页面，现在包含父目录属性"""
    properties = {
        "Name": {"title": [{"text": {"content": os.path.basename(path)}}]},
        "Path": {"rich_text": [{"text": {"content": path}}]},
        "Type": {"select": {"name": "Folder" if is_folder else "File"}},
        "Parent": {"rich_text": [{"text": {"content": parent_path or "Root"}}]}  # 添加 Parent 属性
    }
    try:
        notion.pages.create(parent={"database_id": database_id}, properties=properties)
        print(f"Created Notion page for {path} under {parent_path}")
    except Exception as e:
        print(f"Failed to create Notion page for {path}: {e}")


def create_notion_records_for_directory(database_id, items):
    """并发向Notion数据库添加目录中的文件和文件夹记录"""
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 创建文件夹记录
        folder_futures = [executor.submit(create_page, database_id, folder_path, True) for folder_path in
                          items['folders']]
        # 创建文件记录
        file_futures = [executor.submit(create_page, database_id, file_path) for file_path in items['files']]
        # 等待所有任务完成
        concurrent.futures.wait(folder_futures + file_futures, return_when=concurrent.futures.ALL_COMPLETED)


if __name__ == "__main__":
    # 示例：调用这个函数以开始创建记录
    # 注意：这里需要替换为你实际的目录路径和项目结构
    items_example = {
        'folders': ['/path/to/folder1', '/path/to/folder2'],
        'files': ['/path/to/folder1/file1.txt', '/path/to/folder2/file2.txt']
    }
    create_notion_records_for_directory(DATABASE_ID, items_example)
