from openai import AsyncOpenAI
import requests
import json
import DiscordToken #Delete this..
from discord.ext import commands
import utilities as ut

SQL = 'chat_history.db'

#----------------------------------------------------------------------------------------------------------
@commands.hybrid_command(description="start chat!")
async def totomi(ctx, *, prompt: str):
    with open('config.json', 'r') as file:
        data = json.load(file)

    systemP = data['systemPrompt']
    model = data['model']
    normalModeContextLength = data['normalModeContextLength']
    threadModeContextLength = data['threadModeContextLength']
    if ctx.guild == None:
        guild = 'DM'
    else:
        guild = str(ctx.guild.id)

    prompt = 'From user ' + f'<@{str(ctx.author.id)}>: ' + prompt 
    context = ut.get_latest_guild_messages(str(ctx.channel.id), guild, normalModeContextLength)
    ut.save_guild_message(str(ctx.channel.id), guild, str(ctx.author.id), prompt)

    if model == 'ollama':
        try:
            url = 'http://localhost:11434/api/chat'
            data = compileOllamaPost(prompt=prompt, system = systemP)
            post = requests.post(url, json=data)
            jsondata = post.json()
            await ctx.send(jsondata['message']['content'])
        except Exception as e:
            await ctx.send(str(e))

    if model == 'gpt-3.5-turbo' or model == 'gpt-4o' or model == 'gpt-4-turbo':
        try:
            data = await chatGPTPOST(prompt = prompt, system = systemP, 
                                     model = model, context = context, ctx = ctx)
            await ctx.send(data.choices[0].message.content)
            if ctx.guild == None:
                guild = 'DM'
            else:
                guild = str(ctx.guild.id)
            ut.save_guild_message(str(ctx.channel.id), guild, str(ctx.me.id), data.choices[0].message.content)
        except Exception as e:
            await ctx.send(str(e))

    return
#----------------------------------------------------------------------------------------------------------

@commands.hybrid_command(description="Set the model to either 'chatgpt' or 'ollama'.")
async def usemodel(ctx, model: str):
    with open('config.json','r') as file:
        data = json.load(file)
        data['model'] = model
        await ctx.send(f'Changed model to {model}')
        with open('config.json', 'w') as file:
            json.dump(data, file)
    return
#----------------------------------------------------------------------------------------------------------

@commands.hybrid_command(description="help")
async def help(ctx):
    with open('config.json', 'r') as file:
        data = json.load(file)
    cmds = data['commands']
    txt = ''
    for each in cmds:
        txt = txt + each['description'] + '\n\n'
    await ctx.send(txt)
    return

#----------------------------------------------------------------------------------------------------------

@commands.hybrid_command(description = 'Change context length')
async def set_context_length(ctx, mode:str, length:str):
    with open('config.json', 'r') as file:
        data = json.load(file)

    if mode == 'normal':
        data['normalModeContextLength'] = length
        await ctx.send(f'Set Normal mode context length to: {length}')

    if mode == 'thread':
        data['threadModeContextLength'] = length
        await ctx.send(f'Set Normal mode context length to: {length}')
    return

#----------------------------------------------------------------------------------------------------------
#HELPERS
#----------------------------------------------------------------------------------------------------------
async def chatGPTPOST(**kwargs):
    msg = [
            {'role': 'system', 'content': kwargs['system']}
        ]
    for each in kwargs['context']:
        if each[0] == str(kwargs['ctx'].me.id):
            msg.append(
                {'role': 'assistant', 'content': each[1]}
            )
        else:
            msg.append(
                {'role': 'user', 'content': each[1]}
            )
    msg.append({"role": "user", "content": kwargs['prompt']})
    openaiClient = AsyncOpenAI(api_key=DiscordToken.openAI())
    stream = await openaiClient.chat.completions.create(
        model=kwargs['model'],
        messages = msg,
        stream=False
    )
    return stream
#----------------------------------------------------------------------------------------------------------
async def claudePOST(**kwargs):
    prompt = ''
    for x in kwargs['prompt']:
        prompt = prompt + x + ' '

    data = {
        'model':kwargs['model'],
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