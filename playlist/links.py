import re
import logging
import requests

logger = logging.getLogger('playlist')

def get_links(message):
    stdLink =  list(re.findall(r'spotify\.com\/track\/([\w\d]+)', message))
    auxLink = list(re.findall(r'spotify\.link\/([\w\d]+)', message))
    if auxLink:
        for link in auxLink:
            originalURL = "https://spotify.link/"+link
            ConvertedURL = requests.get(originalURL)
            bigChungus = list(re.findall(r'spotify\.com\/track\/([\w\d]*)', ConvertedURL.url))
            stdLink += bigChungus

    if stdLink:
        logger.debug(stdLink)

    return stdLink
    