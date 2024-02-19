import os
from datetime import datetime

import requests


def get_files_from_folder(folder_path):
    all_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            all_files.append(os.path.join(root, file))
    return all_files


def get_file_info(file_path):
    """获取文件的创建日期和大小"""
    stat = os.stat(file_path)
    create_date = datetime.fromtimestamp(stat.st_ctime).isoformat()
    size = stat.st_size
    return create_date, size


def add_file_to_notion(api_key, database_id, file_path, create_date, size):
    file_name = os.path.basename(file_path)
    file_link = generate_link(file_path)  # 生成链接

    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2021-05-13"
    }

    data = {
        "parent": {"database_id": database_id},
        "properties": {
            "Name": {
                "title": [{"text": {"content": file_name}}]
            },
            "createDate": {
                "date": {"start": create_date}
            },
            "fileSize": {
                "number": size
            },
            "link": {  # 确保与Notion数据库中的属性名匹配
                "url": file_link
            }
        }
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print(f"文件 '{file_name}' 和链接 '{file_link}' 成功添加到Notion数据库.")
    else:
        print(f"错误: {response.status_code}, 详情: {response.text}")


def update_page(api_key, page_id, file_name, create_date, size):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    file_link = generate_link(file_path)  # 生成链接
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2021-05-13"
    }
    data = {
        "properties": {
            "Name": {
                "title": [{"text": {"content": file_name}}]
            },
            "createDate": {
                "date": {"start": create_date}
            },
            "fileSize": {
                "number": size
            },
            "link": {  # 确保与Notion数据库中的属性名匹配
                "url": file_link
            }
        }
    }
    response = requests.patch(url, headers=headers, json=data)
    if response.status_code == 200:
        print(f"文件 '{file_name}' 更新成功.")
    else:
        print(f"更新失败: {response.status_code}, 详情: {response.text}")


def query_for_file(api_key, database_id, file_name):
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2021-05-13"
    }
    data = {
        "filter": {
            "property": "Name",
            "title": {
                "equals": file_name
            }
        }
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        print(f"查询失败: {response.status_code}, 详情: {response.text}")
        return None
    result = response.json()
    return result['results']


def generate_link(file_path):
    base_path = r"C:\Users\dell\Desktop\share"
    web_base_url = "http://124.221.249.173:6443/static"
    relative_path = file_path.replace(base_path, "").replace("\\", "/")
    full_url = web_base_url + relative_path
    return full_url


def update_or_create_page(api_key, database_id, file_path):
    create_date, size = get_file_info(file_path)
    existing_pages = query_for_file(api_key, database_id, file_path)  # 使用完整路径进行查询

    if existing_pages:
        # 如果存在，更新第一个找到的条目
        page_id = existing_pages[0]['id']
        update_page(api_key, page_id, file_path, create_date, size)  # 传递完整路径
    else:
        # 如果不存在，创建新条目
        add_file_to_notion(api_key, database_id, file_path, create_date, size)  # 传递完整路径


img_files = get_files_from_folder(r"C:\Users\dell\Desktop\share\BaiduSyncdisk\IMG")
NOTION_API_KEY = 'secret_SSsAzrzOhICxv9z7KUffGrsgYYOJTpZtNSq59gYhkxs'
DATABASE_ID = '02894238ab214322aaeedc9e1e6d6c81'

for file_path in img_files:
    update_or_create_page(NOTION_API_KEY, DATABASE_ID, file_path)
