from discord.ext import commands
from discord import app_commands
import discord
import utilities as ut
import asyncio
import yt_dlp


FFMPEG_OPTIONS = {
        'before_options':
        '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -probesize 200M',
    }
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

class YTDL(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.playlist = []

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

    async def play_next(self, ctx):
        try:
            url = self.playlist.pop(0)
        except IndexError:
            await ctx.voice_client.disconnect()
            return
        channel = ctx.author.voice.channel
        if channel and not ctx.voice_client:
            voice_client = await channel.connect()
        else:
            voice_client = ctx.voice_client
        with yt_dlp.YoutubeDL(YDL_OPT) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info['title']
            stream_url = info['url']

        await ctx.send(f':musical_note: Playing: {title}')
        audio = discord.FFmpegPCMAudio(
            source=stream_url,
            before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -probesize 200M',
            options='-vn'
        )
        voice_client.play(audio, after=lambda e: self.bot.loop.create_task(self.continue_play(ctx)))

    async def continue_play(self, ctx):
        await self.play_next(ctx)

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

    @commands.hybrid_command(description = 'skip current song')
    async def skip(self, ctx):
        ut.logRequest(ctx)
        if not ctx.voice_client == None and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            if len(self.playlist) == 1:
                await ctx.send('Playlist finished.')
                return
            await ctx.send('Skipped song.')
            return
        else:
            await ctx.send('im not in a voice channel')
        return

    @commands.command(description = 'Play test music')
    async def playLocal(self, ctx, url:str):
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