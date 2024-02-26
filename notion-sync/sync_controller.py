# sync_controller.py
from data_storage import DataStorage
from local_watcher import LocalWatcher
from notion_watcher import NotionWatcher
from notion_api import NotionAPI
from logger import Logger
import threading
import queue
import time


class SyncController:
    def __init__(self, data_storage: DataStorage, notion_api: NotionAPI, logger: Logger):
        self.data_storage = data_storage
        self.notion_api = notion_api
        self.logger = logger
        self.event_queue = queue.Queue()
        self.local_watcher = LocalWatcher(self.event_queue, self.data_storage, self.logger)
        self.notion_watcher = NotionWatcher(self.event_queue, self.data_storage, self.logger)
        self.stop_event = threading.Event()

    def start(self):
        """启动同步控制器，开始监听本地和Notion的变化"""
        self.local_watcher.start()
        self.notion_watcher.start()
        self.logger.log("SyncController started.")

        try:
            while not self.stop_event.is_set():
                try:
                    # 获取事件
                    event = self.event_queue.get(timeout=1)
                    self.handle_event(event)
                except queue.Empty:
                    continue
        finally:
            self.local_watcher.stop()
            self.notion_watcher.stop()

    def handle_event(self, event):
        """处理事件，同步本地文件系统和Notion"""
        if event['source'] == 'local':
            self.sync_local_to_notion(event)
        elif event['source'] == 'notion':
            self.sync_notion_to_local(event)

    def sync_local_to_notion(self, event):
        """处理本地事件，同步到Notion"""
        # 示例逻辑：如果本地创建了文件，就在Notion创建对应页面
        if event['type'] == 'created':
            local_path = event['path']
            notion_id = self.notion_api.create_page(local_path)
            if notion_id:
                self.data_storage.update_mapping(local_path, notion_id)
                self.logger.log(f"Created Notion page for {local_path} with id {notion_id}.")
            else:
                self.logger.log(f"Failed to create Notion page for {local_path}.", level='error')

    def sync_notion_to_local(self, event):
        """处理Notion事件，同步到本地文件系统"""
        # 示例逻辑：如果Notion创建了新页面，就在本地创建对应文件夹
        if event['type'] == 'created':
            notion_id = event['id']
            local_path = self.notion_api.get_page_path(notion_id)
            if local_path:
                self.local_watcher.create_folder(local_path)
                self.data_storage.update_mapping(local_path, notion_id)
                self.logger.log(f"Created local folder for Notion page id {notion_id}.")
            else:
                self.logger.log(f"Failed to retrieve path for Notion page id {notion_id}.", level='error')

    def stop(self):
        """停止同步控制器"""
        self.stop_event.set()
        self.logger.log("SyncController stopped.")


