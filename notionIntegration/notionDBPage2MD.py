# notionDBPage2MD.py
import json
import os
import re

import requests

from findPagesWithContent import get_id_with_contents

# 从配置文件加载配置
with open('../configs/notionIntConfig.json', 'r', encoding='utf-8') as file:
    CONFIGURATION = json.load(file)
    DATABASE_ID = CONFIGURATION['DATABASE']['TXT']
    NOTION_TOKEN = CONFIGURATION["NOTION_TOKEN"]
    SYNC_PATH_DELL = CONFIGURATION['syncPATH']['dell']

HEADERS = {
    'Authorization': f'Bearer {NOTION_TOKEN}',
    'Notion-Version': '2021-05-13'
}


def notion_block_to_markdown(block):
    """
    将单个Notion块转换为Markdown。
    """
    block_type = block['type']
    markdown = ""

    if block_type == 'paragraph':
        if 'text' in block['paragraph']:
            for text_content in block['paragraph']['text']:
                markdown += text_content['plain_text']
        markdown += "\n\n"

    elif block_type == 'heading_1':
        markdown = "# " + block['heading_1']['text'][0]['plain_text'] + "\n\n"

    elif block_type == 'heading_2':
        markdown = "## " + block['heading_2']['text'][0]['plain_text'] + "\n\n"

    elif block_type == 'heading_3':
        markdown = "### " + block['heading_3']['text'][0]['plain_text'] + "\n\n"

    elif block_type == 'bulleted_list_item':
        markdown = "- " + block['bulleted_list_item']['text'][0]['plain_text'] + "\n"

    elif block_type == 'numbered_list_item':
        markdown = "1. " + block['numbered_list_item']['text'][0]['plain_text'] + "\n"

    elif block_type == 'to_do':
        checked = "x" if block['to_do']['checked'] else " "
        markdown = f"- [{checked}] " + block['to_do']['text'][0]['plain_text'] + "\n"

    elif block_type == 'toggle':
        markdown = "> " + block['toggle']['text'][0]['plain_text'] + "\n\n"

    elif block_type == 'code':
        language = block['code']['language']
        code_text = block['code']['text'][0]['plain_text']
        markdown = f"```{language}\n{code_text}\n```\n\n"

    elif block_type == 'image':
        image_url = block['image']['file']['url']
        markdown = f"![Image]({image_url})\n\n"

    # 添加更多类型的转换逻辑...

    return markdown


def fetch_page_title_and_content(page_id):
    """
    获取页面标题和内容
    """
    page_url = f"https://api.notion.com/v1/pages/{page_id}"
    response = requests.get(page_url, headers=HEADERS)
    page_data = response.json()
    title = page_data["properties"]["DellPath"]["title"][0]["plain_text"]

    blocks_query_url = f'https://api.notion.com/v1/blocks/{page_id}/children'
    response = requests.get(blocks_query_url, headers=HEADERS)
    blocks = response.json().get('results', [])

    markdown_content = ""
    for block in blocks:
        markdown_content += notion_block_to_markdown(block)

    return title, markdown_content


def save_markdown(title, content, sync_path):
    """
    保存Markdown内容到本地文件
    """
    # 确保目录存在
    os.makedirs(sync_path, exist_ok=True)
    file_path = os.path.join(sync_path, f"{title}.md")

    with open(file_path, 'w', encoding='utf-8') as md_file:
        md_file.write(content)

    print(f"Markdown file saved to {file_path}")
    return file_path


def update_page_title(page_id, new_title):
    """
    更新Notion页面的DellPath属性为本地文件路径。
    """
    update_url = f'https://api.notion.com/v1/pages/{page_id}'
    data = {
        "properties": {
            "DellPath": {  # 确认这是正确的属性名称
                "title": [
                    {
                        "text": {
                            "content": new_title
                        }
                    }
                ]
            }
        }
    }
    response = requests.patch(update_url, headers=HEADERS, json=data)
    if response.status_code == 200:
        print(f"Page {page_id} title updated successfully to: {new_title}")
        return True
    else:
        print(f"Failed to update page {page_id} title. Status Code: {response.status_code}, Response: {response.text}")
        return False


def sanitize_title(title):
    """
    清洗标题以用作文件名，保留中文、字母、数字和一些特定符号。
    """
    # 正则表达式匹配中文字符、字母、数字和._-符号
    pattern = re.compile(r'[^a-zA-Z0-9\u4e00-\u9fa5._-]+')
    sanitized = pattern.sub('', title)
    return sanitized


def main():
    page_ids = get_id_with_contents(DATABASE_ID)

    for page_id in page_ids:
        title, markdown_content = fetch_page_title_and_content(page_id)

        # 使用sanitize_title函数清洗标题
        sanitized_title = sanitize_title(title)
        file_name = f"{sanitized_title}.md"
        file_path = os.path.join(SYNC_PATH_DELL, file_name)

        # 保存Markdown内容到文件
        save_markdown_path = save_markdown(title, markdown_content, SYNC_PATH_DELL)

        # 根据保存的Markdown文件路径更新Notion页面标题
        update_page_title(page_id, save_markdown_path)


if __name__ == "__main__":
    main()
