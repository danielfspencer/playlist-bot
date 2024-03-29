import sys
import json
import logging

logger = logging.getLogger('playlist')
CONFIG_PATH = 'creds.json'

def init():
    global creds
    logger.info('Loading config...')

    try:
        with open(CONFIG_PATH) as file:
            try:
                creds = json.load(file)
            except json.decoder.JSONDecodeError:
                fatal(f"↳ Cannot parse '{CONFIG_PATH}'")

    except OSError:
        fatal(f"↳ Cannot open '{CONFIG_PATH}'")

def fatal(message):
    logger.critical(message)
    sys.exit(1)
