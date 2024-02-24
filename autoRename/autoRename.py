# autoRename.py
import datetime
import os
import re


def extract_date_prefix(folder_name):
    """尝试从文件夹名称中提取日期前缀，并返回无日期前缀的文件夹名和日期（如果存在）。"""
    match = re.match(r"(\d{8})_(.*)", folder_name)
    if match:
        date_str = match.group(1)
        rest_of_name = match.group(2)
        return date_str, rest_of_name
    else:
        return None, folder_name


def get_average_file_date(folder_path):
    """计算文件夹中所有文件创建时间的平均值，并返回格式化的日期字符串。"""
    timestamps = []
    for filename in os.listdir(folder_path):
        if filename.startswith('.') or filename.startswith('_'):  # 忽略隐藏文件和以'.'或'_'开头的文件
            continue
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):  # 确保是文件
            stats = os.stat(file_path)
            timestamps.append(stats.st_mtime)  # 修改时间作为代替

    if timestamps:
        avg_timestamp = sum(timestamps) / len(timestamps)
        return datetime.datetime.fromtimestamp(avg_timestamp).strftime("%Y%m%d")
    else:
        return None


def rename_folders_in_directory(directory_path, exclude_folder_list):
    """遍历指定目录，更新文件夹的日期前缀基于子文件的平均时间。"""
    for root, dirs, files in os.walk(directory_path, topdown=True):  # 修改为topdown=True以先处理顶层目录
        # 忽略隐藏文件夹和以'.'或'_'开头的文件夹
        dirs[:] = [d for d in dirs if not d.startswith('.') and not d.startswith('_') and d not in exclude_folder_list]

        for folder_name in dirs:
            folder_path = os.path.join(root, folder_name)
            original_date, clean_name = extract_date_prefix(folder_name.replace(' ', '_'))
            avg_date = get_average_file_date(folder_path)

            if avg_date and (avg_date != original_date):
                new_folder_name = f"{avg_date}_{clean_name}"
                new_folder_path = os.path.join(root, new_folder_name)
                print(f"Renaming '{folder_path}' to '{new_folder_path}'")  # 预览重命名操作
                os.rename(folder_path, new_folder_path)  # 执行重命名
            else:
                # 如果平均日期与原日期相同或无法计算平均日期，只更新空格为下划线（如果有必要）
                if folder_name != clean_name:
                    new_folder_path = os.path.join(root, clean_name)
                    print(f"Updating '{folder_path}' to '{new_folder_path}'")  # 预览更新操作
                    os.rename(folder_path, new_folder_path)  # 执行更新


# 示例调用
rename_folders_in_directory(r"C:\Users\dell\Desktop\share\BaiduSyncdisk\SPrint", [])
