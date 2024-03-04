import requests

# 替换为你的Notion Integration Token和数据库ID
notion_token = "secret_SSsAzrzOhICxv9z7KUffGrsgYYOJTpZtNSq59gYhkxs"
database_id = "b4c45205ab4a4d30be8d4f20c157b49f"
headers = {
    "Authorization": f"Bearer {notion_token}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

# 查询数据库
query_url = f"https://api.notion.com/v1/databases/{database_id}/query"
response = requests.post(query_url, headers=headers)

if response.status_code == 200:
    data = response.json()
    for page in data["results"]:
        page_id = page["id"]
        # 假设name属性是一个标题属性
        original_name = page["properties"]["Name"]["title"][0]["text"]["content"]
        # 替换空格为下划线
        new_name = original_name.replace(" ", "_")

        # 构建更新请求的payload
        update_payload = {
            "properties": {
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": new_name
                            }
                        }
                    ]
                }
            }
        }

        # 更新页面
        update_url = f"https://api.notion.com/v1/pages/{page_id}"
        update_response = requests.patch(update_url, headers=headers, json=update_payload)
        if update_response.status_code == 200:
            print(f"Page {original_name} updated to {new_name}")
        else:
            print(f"Failed to update page {original_name}")
else:
    print("Failed to query database")
