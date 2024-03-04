import tkinter as tk
from tkinter import filedialog

from autoFormatClassification import load_file_types, build_extension_mapping, classify_files
from autoRenameFolder import rename_folders_in_directory


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('文件处理工具')
        self.geometry('500x300')

        # 创建界面组件
        self.create_widgets()

    def create_widgets(self):
        # 分类文件的按钮和输入
        self.classify_button = tk.Button(self, text="分类文件", command=self.classify_files_ui)
        self.classify_button.pack(pady=10)

        # 重命名文件夹的按钮
        self.rename_button = tk.Button(self, text="重命名文件夹", command=self.rename_folders_ui)
        self.rename_button.pack(pady=10)

    def classify_files_ui(self):
        # 选择文件夹路径
        folder_path = filedialog.askdirectory(title="选择文件夹")
        json_file_path = filedialog.askopenfilename(title="选择JSON类型文件", filetypes=[("JSON files", "*.json")])
        target_folder_path = filedialog.askdirectory(title="选择目标文件夹路径")

        if folder_path and json_file_path and target_folder_path:
            file_types = load_file_types(json_file_path)
            extension_to_type = build_extension_mapping(file_types)
            classify_files(folder_path, target_folder_path, extension_to_type)

    def rename_folders_ui(self):
        # 选择目录路径
        directory_path = filedialog.askdirectory(title="选择目录")
        if directory_path:
            rename_folders_in_directory(directory_path, [])


if __name__ == "__main__":
    app = Application()
    app.mainloop()
