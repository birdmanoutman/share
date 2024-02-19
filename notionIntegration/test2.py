import requests


def add_file_to_notion(api_key, database_id, file_name):
    url = "https://api.notion.com/v1/pages"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2021-05-13"
    }

    data = {
        "parent": {"database_id": database_id},
        "properties": {
            "Name": {  # 假设数据库中有一个标题属性名为“Name”
                "title": [
                    {
                        "text": {
                            "content": file_name
                        }
                    }
                ]
            }
        }
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print(f"文件名 '{file_name}' 成功添加到Notion数据库.")
    else:
        print(f"错误: {response.status_code}, 详情: {response.text}")


# 示例使用
api_key = "secret_SSsAzrzOhICxv9z7KUffGrsgYYOJTpZtNSq59gYhkxs"
database_id = "2bfff87d518448bab1030a3ad8f189cd"
file_name = "example.txt"  # 假设您想添加的文件名

add_file_to_notion(api_key, database_id, file_name)
