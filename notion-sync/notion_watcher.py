# notion_watcher.py
import requests
import threading
import time
from datetime import datetime


class NotionWatcher:
    def __init__(self, event_queue, data_storage, logger, notion_token, database_id, poll_interval=60):
        self.event_queue = event_queue
        self.data_storage = data_storage
        self.logger = logger
        self.notion_token = notion_token
        self.database_id = database_id
        self.poll_interval = poll_interval
        self.stop_event = threading.Event()
        self.last_sync_time = datetime.now().isoformat()

    def poll_notion_changes(self):
        """检查Notion数据库中的页面变更。"""
        headers = {
            'Authorization': f'Bearer {self.notion_token}',
            'Notion-Version': '2021-05-13'
        }

        # 确保last_sync_time是符合Notion API要求的格式
        # Notion API 需要一个以Z结尾的ISO 8601格式的字符串
        if not self.last_sync_time.endswith('Z'):
            self.last_sync_time += 'Z'

        query = {
            "filter": {
                "property": "Last edited time",
                "last_edited_time": {
                    "after": self.last_sync_time
                }
            }
        }

        try:
            response = requests.post(f'https://api.notion.com/v1/databases/{self.database_id}/query', json=query, headers=headers)
            if response.status_code == 200:
                pages = response.json().get('results', [])
                for page in pages:
                    page_id = page['id']
                    last_edited_time = page['last_edited_time']
                    self.event_queue.put({'source': 'notion', 'type': 'updated', 'page_id': page_id})
                    self.logger.log(f"Detected Notion update: {page_id} at {last_edited_time}")
                    self.last_sync_time = max(self.last_sync_time, last_edited_time)
            else:
                self.logger.log(f"Failed to poll Notion changes: {response.text}", level='error')
        except requests.RequestException as e:
            self.logger.log(f"Error polling Notion API: {e}", level='error')

    def start(self):
        self.logger.log("NotionWatcher started.")
        while not self.stop_event.is_set():
            self.poll_notion_changes()
            time.sleep(self.poll_interval)

    def stop(self):
        self.stop_event.set()
        self.logger.log("NotionWatcher stopped.")

