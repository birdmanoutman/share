import datetime
import os


def get_folder_date(folder_name):
    """尝试从文件夹名称中解析日期，支持多种日期格式"""
    date_formats = [
        "%Y%m%d",  # YYYYMMDD
        "%d%m%Y",  # DDMMYYYY
        "%m%d%Y"  # MMDDYYYY
    ]
    for date_format in date_formats:
        try:
            return datetime.datetime.strptime(folder_name[:8], date_format)
        except ValueError:
            continue
    return None


def rename_folders_in_directory(directory_path, exclude_folder_list):
    for root, dirs, files in os.walk(directory_path, topdown=False):
        for folder_name in dirs:
            if folder_name in exclude_folder_list:
                continue

            folder_path = os.path.join(root, folder_name)
            birth_time = os.stat(folder_path).st_birthtime
            cdate = datetime.datetime.fromtimestamp(birth_time).strftime("%Y%m%d")

            folder_date = get_folder_date(folder_name)
            if folder_date:
                new_folder_name = folder_name
            else:
                # 如果文件夹名不包含有效日期，则使用创建日期作为新名称的一部分
                new_folder_name = cdate + " " + folder_name

            new_folder_path = os.path.join(root, new_folder_name.replace('  ', ' '))
            print(f"Renaming '{folder_path}' to '{new_folder_path}'")  # 预览重命名操作
            # os.rename(folder_path, new_folder_path)  # 执行重命名

# 示例调用
# rename_folders_in_directory("/path/to/directory", ['exclude_folder1', 'exclude_folder2'])
