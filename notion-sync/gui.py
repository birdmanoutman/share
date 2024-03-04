import threading
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
            self.update_status("Syncing...")
            # 使用线程来避免阻塞GUI，并调用SyncController的start方法
            threading.Thread(target=self.sync_controller.start, daemon=True).start()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.update_status("Error")

    def stop_sync(self):
        try:
            self.sync_controller.stop()
            self.update_status("Stopped")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.update_status("Error")

    def update_status(self, status):
        # 更新状态标签的文本
        self.status_label.config(text=status)
