import re
import logging

logger = logging.getLogger('playlist')

def get_links(message):
    matches =  re.findall(r'spotify\.com\/track\/([\w\d]*)', message)

    if matches:
        logger.debug(list(matches))

    return matches
