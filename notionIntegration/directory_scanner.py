import os
from collections import deque


def scan_directory(path):
    """非递归扫描指定目录下的所有文件和文件夹"""
    items = {'folders': [], 'files': []}
    queue = deque([path])

    while queue:
        current_path = queue.popleft()
        try:
            for entry in os.scandir(current_path):
                if entry.is_dir():
                    items['folders'].append(entry.path)
                    queue.append(entry.path)
                else:
                    items['files'].append(entry.path)
        except PermissionError:
            print(f"无权限访问：{current_path}")
        except Exception as e:
            print(f"访问{current_path}时发生错误：{e}")
    return items
