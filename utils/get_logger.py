import logging
import os
from logging.handlers import RotatingFileHandler


class Logger(object):
    """
    A class for managing loggers
    """

    @staticmethod
    def get_console_logger():
        logger = logging.getLogger("lokesh1729")
        formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)
        return logger

    @staticmethod
    def get_file_logger():
        LOGGER_FILE = os.path.join(os.getcwd(), 'my_logger.log')
        logger = logging.getLogger("mine")
        formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
        handler = RotatingFileHandler(LOGGER_FILE, maxBytes=5 * 1024 * 1024,
                                      backupCount=2)
        handler.setFormatter(formatter)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)
        return logger
