import logging
import os
import common
from os.path import join


class Logger():
    log_dir = join(common.root_dir(), 'logs')
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename=join(log_dir, 'log.txt'))
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s @ '
        '%(filename)s:%(funcName)s:%(lineno)s] %(process)s - %(message)s')

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    @staticmethod
    def log(msg):
        Logger.logger.info(msg)
