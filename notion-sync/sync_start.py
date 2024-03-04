import json
from data_storage import DataStorage
from logger import Logger
from notion_api import NotionAPI
from sync_controller import SyncController
from local_watcher import LocalWatcher
from notion_watcher import NotionWatcher
from config_manager import ConfigManager
from queue import Queue


def main():
    # 初始化配置管理器
    config_manager = ConfigManager('config.json')

    # 获取 Notion API 密钥和数据库 ID
    notion_token = config_manager.get('notion_token')
    database_id = config_manager.get('database_id')
    print(f"notion_token:{notion_token}\ndatabase_id:{database_id}")

    local_watch_path = config_manager.get('watch_directory')

    # 实例化Logger
    logger = Logger()

    # 实例化DataStorage
    data_storage = DataStorage()

    # 实例化NotionAPI
    notion_api = NotionAPI(notion_token)

    event_queue = Queue()

    # 实例化LocalWatcher和NotionWatcher
    local_watcher = LocalWatcher(event_queue, data_storage, logger, local_watch_path)
    notion_watcher = NotionWatcher(event_queue, data_storage, logger, notion_token, database_id)

    # 实例化SyncController
    sync_controller = SyncController(data_storage, notion_api, logger, local_watcher, notion_watcher)

    # 启动同步控制器
    sync_controller.start()


if __name__ == '__main__':
    main()
