import os
import re


def rename_files_in_folder(folder_path):
    # 遍历指定文件夹内的所有文件
    for filename in os.listdir(folder_path):
        # 使用正则表达式替换文件名中的空格为下划线
        new_filename = re.sub(r'\s+', '_', filename)

        # 使用正则表达式移除特定符号左右的下划线
        # 符号包括: -, (, ), [, ], {, }
        new_filename = re.sub(r'_(?=[-(){}\[\]])|(?<=[-(){}\[\]])_', '', new_filename)

        # 构建完整的旧文件路径和新文件路径
        old_file_path = os.path.join(folder_path, filename)
        new_file_path = os.path.join(folder_path, new_filename)

        # 重命名文件
        os.rename(old_file_path, new_file_path)

    print("文件名优化完成。")


if __name__ == "__main__":
    rename_files_in_folder(folder_path=r'C:\Users\dell\Desktop\share\Syncdisk\TXT')
