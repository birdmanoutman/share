from sync_controller import SyncController
from config_manager import ConfigManager
from logger import Logger
from notion_api import NotionAPI
from data_storage import DataStorage
import tkinter as tk
from gui import SyncApp


# 初始化配置管理器
config_manager = ConfigManager('config.json')

# 创建日志记录器实例
logger = Logger()

# 初始化数据存储
data_storage = DataStorage()

# 获取Notion API密钥
notion_api_key = config_manager.get('notion_api_key')

# 使用Notion API密钥初始化NotionAPI实例
notion_api = NotionAPI(notion_api_key)

# 获取 Notion API 密钥和数据库 ID
notion_token = config_manager.get('notion_token')
database_id = config_manager.get('database_id')
print(f"notion_token:{notion_token}\ndatabase_id:{database_id}")
# 初始化同步控制器
sync_controller = SyncController(data_storage, notion_api, logger, notion_token, database_id)

# 启动GUI
root = tk.Tk()
app = SyncApp(root, sync_controller)
root.mainloop()
