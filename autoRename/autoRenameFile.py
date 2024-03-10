import os


def rename_files_in_folder(folder_path):
    # 遍历指定文件夹内的所有文件
    for filename in os.listdir(folder_path):
        # 去除文件名中的多余空格，并用下划线替换空格
        new_filename = '_'.join(filename.split()).translate(str.maketrans("", "", r'\/:*?"<>|'))

        # 构建完整的旧文件路径和新文件路径
        old_file_path = os.path.join(folder_path, filename)
        new_file_path = os.path.join(folder_path, new_filename)

        # 重命名文件
        os.rename(old_file_path, new_file_path)

    print("文件名优化完成。")


if __name__ == "__main__":
    rename_files_in_folder(folder_path=r'C:\Users\dell\Desktop\share\Syncdisk\TXT')
