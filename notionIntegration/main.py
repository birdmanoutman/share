import threading
from directory_scanner import scan_directory
from notion_integrator import create_notion_records_for_directory
from local_file_opener import app
import json


with open(r'../configs/notionIntConfig.json', 'r', encoding='utf-8') as file:
    configdata = json.load(file)


# Notion配置
DATABASE_ID = configdata['DATABASE']['sprintProjects']
NOTION_TOKEN = configdata['NOTION_TOKEN']

# 本地目录路径
DIRECTORY_PATH = r"/Users/birdmanoutman/DATABASE/SPrint"

# 本地文件打开服务端口
LOCAL_FILE_OPENER_PORT = 5000

def start_local_file_opener_service():
    app.run(port=LOCAL_FILE_OPENER_PORT, debug=False)

def main():
    # 启动本地文件打开服务
    threading.Thread(target=start_local_file_opener_service, daemon=True).start()

    # 扫描本地目录并收集信息
    items = scan_directory(DIRECTORY_PATH)

    # 在Notion中为目录和文件创建记录
    create_notion_records_for_directory(DATABASE_ID, items)

if __name__ == "__main__":
    main()
