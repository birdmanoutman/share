import tkinter as tk
from tkinter import ttk, messagebox

class SyncApp:
    def __init__(self, master, sync_controller):
        self.master = master
        self.sync_controller = sync_controller  # 假设 sync_controller 是一个已经定义好的同步控制器实例

        master.title("Notion Sync Tool")

        # 配置布局
        self.setup_layout()

        # 初始化同步状态
        self.update_status("Ready")

    def setup_layout(self):
        self.start_button = ttk.Button(self.master, text="Start Sync", command=self.start_sync)
        self.start_button.grid(row=0, column=0, padx=10, pady=10)

        self.stop_button = ttk.Button(self.master, text="Stop Sync", command=self.stop_sync)
        self.stop_button.grid(row=0, column=1, padx=10, pady=10)

        self.status_label = ttk.Label(self.master, text="")
        self.status_label.grid(row=1, column=0, columnspan=2)

    def start_sync(self):
        try:
            # 假设 start_sync 方法启动同步过程，并接受回调以更新状态
            self.sync_controller.start_sync(self.update_status)
            self.update_status("Syncing...")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.update_status("Error")

    def stop_sync(self):
        # 假设 stop_sync 方法停止同步过程
        self.sync_controller.stop_sync()
        self.update_status("Stopped")

    def update_status(self, status):
        # 更新状态标签的文本
        self.status_label.config(text=status)

# 假设这里有一些方式来获取或创建 sync_controller 实例
# sync_controller = ...

# 创建主窗口
root = tk.Tk()
app = SyncApp(root, sync_controller)
root.mainloop()
