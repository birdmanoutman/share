import json
import os
import shutil


def load_file_types(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data.get("file_types", {})


def classify_files(folder_path, file_types):
    files = os.listdir(folder_path)

    for file in files:
        source_path = os.path.join(folder_path, file)

        if os.path.isfile(source_path):
            file_extension = file.split('.')[-1].lower()

            for file_type, extensions in file_types.items():
                if file_extension in extensions:
                    target_folder = os.path.join(folder_path, file_type)

                    if not os.path.exists(target_folder):
                        os.makedirs(target_folder)

                    target_path = os.path.join(target_folder, file)

                    shutil.move(source_path, target_path)
                    print(f"Moved {file} to {target_folder}")
                    break


if __name__ == "__main__":
    default_folder_path = r'C:\Users\dell\Desktop'
    default_json_file_path = r'FileHub_Flask/file_categories.json'

    folder_path = input(f"Enter the folder path (default: {default_folder_path}): ") or default_folder_path
    json_file_path = input(f"Enter the JSON file path (default: {default_json_file_path}): ") or default_json_file_path

    file_types = load_file_types(json_file_path)
    classify_files(folder_path, file_types)
