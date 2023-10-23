import os
import sys
import logging
import time

LOG_PATH = 'logs'
CONSOLE_LEVEL = logging.DEBUG
FILE_LEVEL = logging.DEBUG

def init():
    os.makedirs(LOG_PATH, exist_ok=True)

    logging.addLevelName(logging.WARNING, 'WARN')
    logging.addLevelName(logging.CRITICAL, 'FATAL')
    logger = logging.getLogger('playlist')
    logger.setLevel(logging.DEBUG)

    console_format = logging.Formatter('%(asctime)s %(levelname)5s %(module)7s: %(message)s', '%H:%M:%S')
    file_format = logging.Formatter('%(asctime)s %(levelname)5s %(module)7s: %(message)s', '%d/%m/%y %H:%M:%S')

    file_handler = logging.FileHandler(filename=f'{LOG_PATH}/{time.strftime("%d-%m-%Y_%H-%M-%S")}.log', encoding='utf-8', mode='w')
    file_handler.setFormatter(file_format)
    file_handler.setLevel(FILE_LEVEL)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_format)
    console_handler.setLevel(CONSOLE_LEVEL)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
