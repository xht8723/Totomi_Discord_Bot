import youtube_dl
import json
from discord.ext import commands
from discord import app_commands
import discord
import utilities as ut
import time
import asyncio

class YTDL(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume = 0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'yesplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': False,
    'no_warnings': False,
    'default_search': 'auto'
}

ffmpeg_options = {
    'options': '-vn'
}

@commands.hybrid_command(description = 'Play youtube music!')
async def play(ctx, url:str):
    channel = ctx.author.voice.channel
    file = 'I_Will_Touch_the_Sky.flac'
    if not channel == None:
        voiceClient = await channel.connect()
        audio = discord.FFmpegPCMAudio(source=file)
        voiceClient.play(audio, after = lambda _:asyncio.run_coroutine_threadsafe(
            coro = voiceClient.disconnect(),
            loop = voiceClient.loop
        ).result())
    return