# findPagesWithContent.py
# 输入数据库id，找到数据库中有内容的title，并返回这些title 对应的Page ID
# 采用了并发请求，参考https://chat.openai.com/share/2cb23ae7-266b-4adf-85c0-cbf0e4d4ec2d
import concurrent.futures
import json
import requests

with open(r'../configs/notionIntConfig.json', 'r', encoding='utf-8') as file:
    configdata = json.load(file)

# 初始化
NOTION_TOKEN = configdata['NOTION_TOKEN']
DATABASE_ID = configdata['DATABASE']['TXT']
HEADERS = {
    'Authorization': f'Bearer {NOTION_TOKEN}',
    'Notion-Version': '2021-05-13'
}


def fetch_blocks(page_id):
    """获取页面的块内容"""
    blocks_query_url = f'https://api.notion.com/v1/blocks/{page_id}/children'
    response = requests.get(blocks_query_url, headers=HEADERS)
    blocks = response.json().get('results', [])
    return len(blocks) > 1, page_id


def get_id_with_contents(database_id):
    # 首先获取数据库中的页面列表
    contentPageID_list = []
    database_query_url = f'https://api.notion.com/v1/databases/{database_id}/query'
    response = requests.post(database_query_url, headers=HEADERS)
    pages = response.json().get('results', [])

    # 使用线程池并发获取每个页面的块
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        future_to_page = {executor.submit(fetch_blocks, page['id']): page for page in pages}
        for future in concurrent.futures.as_completed(future_to_page):
            has_content, page_id = future.result()
            if has_content:
                print(f"Page ID {page_id} has content.")
                contentPageID_list.append(page_id)
    return contentPageID_list


if __name__ == "__main__":
    get_id_with_contents(DATABASE_ID)
