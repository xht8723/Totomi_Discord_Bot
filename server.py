import discord
from openai import AsyncOpenAI
import requests
import json
import DiscordToken #Delete this..
from discord.ext import commands

url = 'http://localhost:11434/api/chat'
systemPrompt = '你的名字叫远江, 你是一个女生，说话语气可爱，你会帮我回答我的问题并且和我聊天，用中文回复所有内容。'
openaiClient = AsyncOpenAI(api_key=DiscordToken.openAI())

#----------------------------------------------------------------------------------------------------------

class Totomi(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initJson()
        self.add_command(totomi)
        self.add_command(usemodel)

    async def on_ready(self):
        try:
            # Sync the commands with Discord
            await self.tree.sync()
            print("Commands synced successfully.")
        except Exception as e:
            print(f"Failed to sync commands: {e}")
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    def initJson(self):
        data = {
            "systemPrompt": systemPrompt,
            "model": "chatgpt"
        }
        with open('data.json', 'w') as file:
            json.dump(data, file)


#----------------------------------------------------------------------------------------------------------

@commands.hybrid_command(description="start chat!")
async def totomi(ctx, *, prompt: str):
    with open('data.json', 'r') as file:
        data = json.load(file)

    systemP = data['systemPrompt']
    model = data['model']

    if model == 'ollama':
        try:
            data = compileOllamaPost(prompt=prompt, system = systemP)
            post = requests.post(url, json=data)
            jsondata = post.json()
            await ctx.send(jsondata['message']['content'])
        except Exception as e:
            await ctx.send(str(e))

    if model == 'chatgpt':
        try:
            data = await chatGPTPOST(prompt = prompt, system = systemP)
            await ctx.send(data.choices[0].message.content)
        except Exception as e:
            await ctx.send(str(e))

#----------------------------------------------------------------------------------------------------------

def compileOllamaPost(**kwargs):
    prompt = ''
    for x in kwargs['prompt']:
        prompt = prompt + x + ' '

    data = {
        'model':'llama3',
        "stream": False,
        'system': kwargs['system'],
        'temperature':0.8,
        'messages': [
            {
                'role':'system',
                'content':kwargs['system']
            },
            {
                'role':'user',
                'content':kwargs['prompt']
            }
        ]
    }
    return data

#-------------------------------------------------------------------------------------------------

async def chatGPTPOST(**kwargs):
    stream = await openaiClient.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'system', 'content': kwargs['system']},
            {"role": "user", "content": kwargs['prompt']},
            ],
        stream=False
    )
    return stream


#----------------------------------------------------------------------------------------------------------

async def claudePOST(**kwargs):
    prompt = ''
    for x in kwargs['prompt']:
        prompt = prompt + x + ' '

    data = {
        'model':'llama3',
        "stream": False,
        'system': kwargs['system'],
        'temperature':0.8,
        'messages': [
            {
                'role':'system',
                'content':kwargs['system']
            },
            {
                'role':'user',
                'content':kwargs['prompt']
            }
        ]
    }
    return data


#----------------------------------------------------------------------------------------------------------

@commands.hybrid_command(description="Set the model to either 'chatgpt' or 'ollama'.")
async def usemodel(ctx, *, model: str):
    with open('data.json','r') as file:
        data = json.load(file)

    if model == 'chatgpt' or model == 'ollama': 
        data['model'] = model
        await ctx.send(f'Changed model to {model}')
        with open('data.json', 'w') as file:
            json.dump(data, file)

#----------------------------------------------------------------------------------------------------------




#----------------------------------------------------------------------------------------------------------
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

client = Totomi(command_prefix='_', intents=intents)
client.run(DiscordToken.totomiT()) #change to your token value
