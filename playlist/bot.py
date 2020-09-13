import csv
import discord
import logging
import subprocess
from discord.ext import commands

from . import config
from . import links
from . import spotify

REPO_LINK = "https://github.com/danielfspencer/playlist-bot"

logger = logging.getLogger('playlist')
bot = discord.ext.commands.Bot(command_prefix=config.creds['discord']['command_prefix'])

tracks = []

def start():
    logger.info("Starting bot...")
    bot.run(config.creds['discord']['token'])

async def rebuild_playlist(ctx):
    await log_and_message(ctx, "Rebuild playlist...")
    discord_tracks = []

    for channel_id in config.creds['discord']['channels']:
        channel = bot.get_channel(channel_id)
        if channel is None:
            logger.warning(f"Skipping non-existent channel '{channel_id}'")
            continue

        if not isinstance(channel, discord.channel.TextChannel):
            logger.warning(f"Skipping non-text channel '{channel_id}'")
            continue

        await log_and_message(ctx, f"Scanning channel '{channel.name}'...")

        async for message in channel.history(limit=None, oldest_first=True):
            if message.author.bot:
                continue

            results = links.get_links(message.clean_content)
            discord_tracks.extend(results)

    await log_and_message(ctx, f"Found {len(discord_tracks)} track(s)")

    await log_and_message(ctx, "Empty playlist...")

    playlist_tracks = spotify.get()
    for track in playlist_tracks:
        spotify.remove(track)
    spotify.flush_remove_buffer()

    await log_and_message(ctx, "Populate playlist...")

    for track in discord_tracks:
        spotify.add(track)
    spotify.flush_add_buffer()

    await log_and_message(ctx, f"Rebuild done")

def get_status():
    message = f"Watching channel(s): {config.creds['discord']['channels']}\n"
    message += spotify.get_status()
    return message

@bot.event
async def on_ready():
    logger.info("Bot online")
    logger.info(f"Status:\n{get_status()}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    await bot.process_commands(message)

    if message.channel.id not in config.creds['discord']['channels']:
        return

    results = links.get_links(message.clean_content)
    if results:
        for result in results:
            spotify.add(result)
        spotify.flush_add_buffer()

async def log_and_message(channel, message):
    logger.info(message)
    await channel.send(message)


@bot.command()
async def status(ctx):
    await ctx.send(get_status())

@bot.command()
async def version(ctx):
    try:
        commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], stderr=subprocess.DEVNULL).decode('ascii').strip()
    except subprocess.CalledProcessError:
        commit = 'unknown, could not run git'

    message = f"Playlist Bot [commit `{commit}`]\n"
    message += f"<{REPO_LINK}>"
    await ctx.send(message)

@bot.command()
async def rebuild(ctx):
    if ctx.author.id in config.creds['discord']['admin_ids']:
        await rebuild_playlist(ctx)
    else:
        logger.warn(f'Unauthorised user \'{ctx.author.display_name}\' ({ctx.author.id}) tried to use rebuild command')
