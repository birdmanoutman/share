# data_storage.py
import json
import threading
from pathlib import Path


class DataStorage:
    def __init__(self, filepath='sync_data.json'):
        self.filepath = Path(filepath)
        self.lock = threading.Lock()
        self.data = self.load_data()

    def load_data(self):
        """加载同步数据。如果文件不存在，则初始化为空字典。"""
        if self.filepath.exists():
            with open(self.filepath, 'r') as file:
                return json.load(file)
        else:
            return {
                'local_to_notion': {},
                'notion_to_local': {},
                'sync_history': []
            }

    def save_data(self):
        """将同步数据保存到文件。使用锁来避免并发写入问题。"""
        with self.lock:
            with open(self.filepath, 'w') as file:
                json.dump(self.data, file, indent=4)

    def get_notion_id(self, local_path):
        """给定本地路径，获取对应的Notion页面ID。"""
        return self.data.get('local_to_notion', {}).get(local_path)

    def get_local_path(self, notion_id):
        """给定Notion页面ID，获取对应的本地路径。"""
        return self.data.get('notion_to_local', {}).get(notion_id)

    def update_mapping(self, local_path, notion_id):
        """更新本地路径和Notion页面ID之间的映射关系。"""
        with self.lock:
            self.data['local_to_notion'][local_path] = notion_id
            self.data['notion_to_local'][notion_id] = local_path
            self.save_data()

    def record_sync_action(self, action_type, local_path=None, notion_id=None, status='success'):
        """记录同步操作的详细信息。"""
        with self.lock:
            action_record = {
                'action_type': action_type,
                'local_path': local_path,
                'notion_id': notion_id,
                'status': status
            }
            self.data['sync_history'].append(action_record)
            self.save_data()


