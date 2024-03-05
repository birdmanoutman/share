import json
from pathlib import Path


class ConfigManager:
    def __init__(self, config_path='config.json'):
        self.config_path = Path(config_path)
        self.config = self.load_config()

    def load_config(self):
        """从文件加载配置。"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file {self.config_path} not found.")

        with open(self.config_path, 'r') as config_file:
            return json.load(config_file)

    def get(self, key, default=None):
        """获取配置项的值。如果不存在，返回默认值。"""
        return self.config.get(key, default)
