import logging
import os
from datetime import datetime

class Logger:
    def __init__(self, name, log_dir="logs"):
        self.log_dir = log_dir
        self.name = name

        # Create logs directory if it doesn't exist
        os.makedirs(log_dir, exist_ok=True)

        # Create logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # File handler
        log_file = os.path.join(
            log_dir,
            f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
        )
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)

        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)

        # Add handler to logger
        if not self.logger.handlers:
            self.logger.addHandler(file_handler)

    def info(self, message):
        self.logger.info(message)

    def error(self, message, exc=None):
        if exc:
            self.logger.error(f"{message}: {exc}", exc_info=True)
        else:
            self.logger.error(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)
