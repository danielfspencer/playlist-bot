import logging
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from . import config

logger = logging.getLogger('playlist')
SCOPE = 'playlist-modify-public'
REDIRECT= 'https://localhost:8080'
MAX_REQUEST_SIZE = 100
PLAYLIST = config.creds['spotify']['playlist_id']

add_buffer = []
remove_buffer = []

def init():
    logger.info("Connecting to Spotify....")
    global instance
    instance = spotipy.Spotify(
        auth_manager=SpotifyOAuth(scope=SCOPE,
        redirect_uri=REDIRECT,
        client_id=config.creds['spotify']['client_id'],
        client_secret=config.creds['spotify']['client_secret'])
        )

def add(item):
    if len(add_buffer) == MAX_REQUEST_SIZE:
        flush_add_buffer()

    add_buffer.append(item)
    logger.debug(f"Append '{item}' to add_buffer ({len(add_buffer)}/{MAX_REQUEST_SIZE})")

def flush_add_buffer():
    global add_buffer
    logger.debug(f"Flushing add_buffer ({len(add_buffer)}/{MAX_REQUEST_SIZE})")
    _add(add_buffer)
    add_buffer = []

def _add(items):
    items.reverse()
    logger.info(f"Adding {len(items)} item(s)")
    logger.debug(f"Adding: {items}")
    instance.playlist_add_items(PLAYLIST, items, 0)

def remove(item):
    if len(remove_buffer) == MAX_REQUEST_SIZE:
        flush_remove_buffer()

    remove_buffer.append(item)
    logger.debug(f"Append '{item}' to remove_buffer ({len(remove_buffer)}/{MAX_REQUEST_SIZE})")

def flush_remove_buffer():
    global remove_buffer
    logger.debug(f"Flushing remove_buffer ({len(remove_buffer)}/{MAX_REQUEST_SIZE})")
    _remove(remove_buffer)
    remove_buffer = []

def _remove(items):
    logger.info(f"Removing {len(items)} item(s)")
    logger.debug(f"Removing: {items}")
    instance.playlist_remove_all_occurrences_of_items(PLAYLIST, items)

def get():
    offset = 0
    tracks = []

    logger.debug("Fetching tracks...")
    while True:
        response = instance.playlist_items(
            PLAYLIST,
            offset=offset,
            fields='items.track.id'
            )

        tracks.extend([item['track']['id'] for item in response['items']])

        response_size = len(response['items'])
        offset += response_size

        if response_size == 0:
            break

    return tracks

def get_status():
    info = instance.current_user()
    status = f"Authorised as: '{info['display_name']}' ({info['external_urls']['spotify']})\n"
    status += f"Playlist: https://open.spotify.com/playlist/{PLAYLIST}"
    return status
