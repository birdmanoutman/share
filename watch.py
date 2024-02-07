import logging
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

# 设置日志配置
logging.basicConfig(filename=r'C:\Users\dell\Desktop\file_operations.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')


class Watcher:
    DIRECTORY_TO_WATCH = r"C:\Users\dell\Desktop\share"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is created.
            logging.info(f"Received created event - {event.src_path}.")

        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            logging.info(f"Received modified event - {event.src_path}.")

        elif event.event_type == 'deleted':
            # Taken any action here when a file is deleted.
            logging.info(f"Received deleted event - {event.src_path}.")

        elif event.event_type == 'moved':
            # Taken any action here when a file is moved.
            logging.info(f"Received moved event - from {event.src_path} to {event.dest_path}")


if __name__ == '__main__':
    w = Watcher()
    w.run()
