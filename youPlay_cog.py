from discord.ext import commands
from discord import app_commands
import discord
import utilities as ut
import asyncio
import yt_dlp
import logging
logger = logging.getLogger('discord')
#-------------------------------------------------------------
# youPlay_cog
# This is a cog module for playing youtube music.
#-------------------------------------------------------------

# yt_dlp options for playing music.
YDL_OPT = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'quiet': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    }

#-------------------------------------------------------------
# class YTDL
# This is the main class for the cog.
# playlist saves song queue.
#-------------------------------------------------------------
class YTDL(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.playlist = []

    #-------------------------------------------------------------
    # play
    # This is a discord command for playing music.
    # Accepting a youtube video url and using yt_dlp to extract playlist and song information.
    #-------------------------------------------------------------
    @commands.hybrid_command(description='Play youtube music!')
    async def play(self, ctx, url: str):
        ut.logRequest(ctx, url)
        await ctx.defer()
        if 'list=' in url:
            with yt_dlp.YoutubeDL({'extract_flat':'in_playlist', 'playlistrandom':True, 'quiet':True}) as ydl:
                info = ydl.extract_info(url, download=False)
            for each in info['entries']:
                self.playlist.append(each['url'])
            await ctx.send(f'Added {len(info["entries"])} songs into queue.')
        else:
            self.playlist.append(url)
            await ctx.send('Added song into queue.')

        if len(self.playlist) >=1 and ctx.voice_client == None:
             await self.play_next(ctx)

    #-------------------------------------------------------------
    # play_next
    # This is a support function to actually starting to play music from the playlist.
    #-------------------------------------------------------------
    async def play_next(self, ctx):
        try:
            url = self.playlist.pop(0)
        except IndexError as e:
            logger.info(e)
            await ctx.voice_client.disconnect()
            return
        channel = ctx.author.voice.channel
        if channel is not None and ctx.voice_client is None:
            voice_client = await channel.connect()
        else:
            voice_client = ctx.voice_client
        try:
            with yt_dlp.YoutubeDL(YDL_OPT) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info['title']
                stream_url = info['url']
        except yt_dlp.DownloadError as e:
            logger.error(e)
            await self.continue_play(ctx)

        await ctx.send(f':musical_note: Playing: {title}')
        audio = discord.FFmpegPCMAudio(
            source=stream_url,
            before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -probesize 200M',
            options='-vn'
        )
        voice_client.play(audio, after=lambda e: self.bot.loop.create_task(self.continue_play(ctx)))

    #-------------------------------------------------------------
    # continue_play
    # This is a support function to recurrently play the next song.
    #-------------------------------------------------------------
    async def continue_play(self, ctx):
        await self.play_next(ctx)

    #-------------------------------------------------------------
    # leave
    # This is a discord command for asking bot to leave the voice channel.
    #-------------------------------------------------------------
    @commands.hybrid_command(description = 'leave voice channel')
    async def leave(self, ctx):
        ut.logRequest(ctx)
        self.playlist.clear()
        if not ctx.voice_client:
            await ctx.send('im not in a voice channel')
            return
        await ctx.voice_client.disconnect()
        await ctx.send('Totomi Out.')
        return

    #-------------------------------------------------------------
    # skip
    # This is a discord command for skipping current playing song.
    #-------------------------------------------------------------
    @commands.hybrid_command(description = 'skip current song')
    async def skip(self, ctx):
        ut.logRequest(ctx)
        if not ctx.voice_client == None:
            ctx.voice_client.stop()
            if len(self.playlist) == 1:
                await ctx.send('Playlist finished.')
                return
            await ctx.send('Skipped song.')
            return
        else:
            await ctx.send('im not in a voice channel')
        return

    #-------------------------------------------------------------
    # playLocal
    # This is a discord command for playing a local music file. This is for testing.
    #-------------------------------------------------------------
    @commands.command(description = 'Play test music')
    async def playLocal(self, ctx, url:str):
        channel = ctx.author.voice.channel
        file = 'tts.mp3'
        if not channel == None:
            voiceClient = await channel.connect()
            audio = discord.FFmpegPCMAudio(source=file)
            voiceClient.play(audio, after = lambda _:asyncio.run_coroutine_threadsafe(
                coro = voiceClient.disconnect(),
                loop = voiceClient.loop
            ).result())
        return
    
    #-------------------------------------------------------------
    # getModelStatus
    # This is a helper function that returns currently using AI model.
    #-------------------------------------------------------------
    @commands.command(description = 'Play personal music')
    async def play84(self, ctx):
        await ctx.invoke(self.play, 'https://www.youtube.com/playlist?list=PL9y52Flm1yM-b2y-JSHQOn_qm4lZnO72F')
        return