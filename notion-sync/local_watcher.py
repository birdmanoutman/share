from watchdog.observers import Observer


class LocalWatcher:
    def __init__(self, event_queue, data_storage, logger, directory_to_watch="/path/to/watch"):
        self.observer = Observer()
        self.event_queue = event_queue
        self.data_storage = data_storage
        self.logger = logger
        self.directory_to_watch = directory_to_watch

    class Handler(FileSystemEventHandler):
        def __init__(self, event_queue, logger):
            self.event_queue = event_queue
            self.logger = logger

        def on_any_event(self, event):
            if event.is_directory:
                return None

            if event.event_type in ('created', 'deleted', 'moved'):
                self.event_queue.put({'source': 'local', 'type': event.event_type, 'path': event.src_path})
                self.logger.log(f"Detected local event: {event.event_type} on {event.src_path}")

    def start(self):
        self.observer.schedule(self.Handler(self.event_queue, self.logger), self.directory_to_watch, recursive=True)
        self.observer.start()
        self.logger.log("LocalWatcher started watching: " + self.directory_to_watch)

    def stop(self):
        self.observer.stop()
        self.observer.join()
        self.logger.log("LocalWatcher stopped.")
