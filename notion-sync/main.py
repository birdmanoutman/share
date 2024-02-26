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

# 创建API连接
notion_api = NotionAPI(config_manager.get_notion_api_key())

# 初始化同步控制器
sync_controller = SyncController(data_storage, notion_api, logger)

# 启动GUI
root = tk.Tk()
app = SyncApp(root, sync_controller)
root.mainloop()
