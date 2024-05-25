import discord
import requests
import DiscordToken #Delete this..
from discord.ext import commands

url = 'http://localhost:11434/api/chat'
systemPrompt = '你的名字叫远江, 你是一个女生，说话语气可爱活泼，你会帮我回答我的问题并且和我聊天，用中文回复所有内容。'
class Totomi(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_command(totomi)

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

@commands.command()
async def totomi(ctx, *args):
    data = compilePOST(args)
    post = requests.post(url, json=data)
    json = post.json()
    await ctx.send(json['message']['content'])


def compilePOST(args):
    prompt = ''
    for x in args:
        prompt = prompt + x + ' '

    data = {
        'model':'llama3',
        "stream": False,
        'system': systemPrompt,
        'temperature':0.8,
        'messages': [
            {
                'role':'system',
                'content':systemPrompt
            },

            {
                'role':'user',
                'content':prompt
            }
        ]
    }
    return data

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

client = Totomi(command_prefix='_', intents=intents)
client.run(DiscordToken.totomiT()) #change to your token value
