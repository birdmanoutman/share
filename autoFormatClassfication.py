import json
import os
import shutil

def load_file_types(file_path):
    """功能：读取并解析一个JSON文件，该文件包含不同类型的文件扩展名及其描述。"""
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data.get("file_types", {})

def build_extension_mapping(file_types):
    """功能：将从JSON文件中读取的数据转换成一个扩展名到文件类型和描述的映射。"""
    extension_to_type = {}
    for file_type, extension_dicts in file_types.items():
        for extension_dict in extension_dicts:
            extension = extension_dict["extension"].lower()  # 确保键值为小写
            extension_to_type[extension] = {
                "type": file_type,
                "description": extension_dict["description"]
            }
    return extension_to_type


def classify_files(folder_path, target_folder_path, extension_to_type):
    """功能：遍历指定文件夹中的所有文件，根据文件扩展名将文件归类到子文件夹中。"""
    files = os.listdir(folder_path)
    for file in files:
        source_path = os.path.join(folder_path, file)
        if os.path.isfile(source_path):
            file_extension = file.split('.')[-1].lower()
            if file_extension in extension_to_type:
                file_info = extension_to_type[file_extension]
                target_folder = os.path.join(target_folder_path, file_info["type"])
                if not os.path.exists(target_folder):
                    os.makedirs(target_folder)
                target_path = os.path.join(target_folder, file)
                shutil.move(source_path, target_path)
                print(f"Moved {file} to {target_folder}. Description: {file_info['description']}")

if __name__ == "__main__":
    default_folder_path = r'G:\20230128_下载backup'
    default_json_file_path = r'FileHub_Flask/file_categories_withDescription.json'

    folder_path = input(f"Enter the folder path (default: {default_folder_path}): ") or default_folder_path
    json_file_path = input(f"Enter the JSON file path (default: {default_json_file_path}): ") or default_json_file_path
    target_folder_path = input(f"Enter the target folder path (default: same as folder path): ") or folder_path

    file_types = load_file_types(json_file_path)
    extension_to_type = build_extension_mapping(file_types)
    classify_files(folder_path, target_folder_path, extension_to_type)
