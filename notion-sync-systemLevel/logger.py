import logging


class Logger:
    def __init__(self, level=logging.INFO):
        self.logger = logging.getLogger("notion_sync_logger")
        self.logger.setLevel(level)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log(self, message, level=logging.INFO):
        if level == logging.ERROR:
            self.logger.error(message)
        else:
            self.logger.info(message)
