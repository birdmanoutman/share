import tkinter as tk
from tkinter import filedialog, messagebox

from autoRenameFolder import rename_folders_in_directory  # 确保这个导入路径根据你的文件结构调整


def select_directory():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        directory_entry.delete(0, tk.END)
        directory_entry.insert(0, folder_selected)


def start_renaming():
    directory_path = directory_entry.get()
    exclude_folders = exclude_entry.get().split(',')
    exclude_folders = [folder.strip() for folder in exclude_folders]
    try:
        rename_folders_in_directory(directory_path, exclude_folders)
        messagebox.showinfo("完成", "文件夹重命名完成")
    except Exception as e:
        messagebox.showerror("错误", f"发生错误: {str(e)}")


app = tk.Tk()
app.title("文件夹重命名工具")

frame = tk.Frame(app)
frame.pack(padx=10, pady=10)

tk.Label(frame, text="目录路径:").pack(side=tk.LEFT)
directory_entry = tk.Entry(frame, width=50)
directory_entry.pack(side=tk.LEFT)
tk.Button(frame, text="浏览", command=select_directory).pack(side=tk.LEFT)

tk.Label(app, text="排除的文件夹（用逗号分隔）:").pack(padx=10, pady=(10, 0))
exclude_entry = tk.Entry(app, width=58)
exclude_entry.pack(padx=10, pady=(0, 10))

tk.Button(app, text="开始重命名", command=start_renaming).pack(pady=(0, 10))

app.mainloop()
