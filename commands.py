from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
import requests
import json
import DiscordToken #Delete this..
from discord.ext import commands
import utilities as ut
import discord

SQL = 'chat_history.db'
MODELS = ['gpt-3.5-turbo', 'gpt-4o', 'gpt-4-turbo', 'ollama', 'claude-3-opus', 'claude-3-sonnet', 'claude-3-haiku']

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

            ut.save_guild_message(str(ctx.channel.id), guild, str(ctx.author.id), prompt)
            ut.save_guild_message(str(ctx.channel.id), guild, str(ctx.me.id), data.choices[0].message.content)
        except Exception as e:
            await ctx.send(str(e))
    
    if model == 'claude-3-opus-20240229' or model == 'claude-3-sonnet-20240229' or model == 'claude-3-haiku-20240307':
        try:
            data = await claudePOST(prompt = prompt, system = systemP, 
                                     model = model, context = context, ctx = ctx)
            await ctx.send(data.content[0].text)
            if ctx.guild == None:
                guild = 'DM'
            else:
                guild = str(ctx.guild.id)

            ut.save_guild_message(str(ctx.channel.id), guild, str(ctx.author.id), prompt)
            ut.save_guild_message(str(ctx.channel.id), guild, str(ctx.me.id), data.content[0].text)
        except Exception as e:
            await ctx.send(str(e))

    return
#----------------------------------------------------------------------------------------------------------

@commands.hybrid_command(description="gpt-3.5-turbo, gpt-4o, gpt-4-turbo, ollama, claude-3-opus, claude-3-sonnet, claude-3-haiku")
async def usemodel(ctx, model: str):
    with open('config.json','r') as file:
        if model in MODELS:
            if model == 'claude-3-opus':
                model = 'claude-3-opus-20240229'
            if model == 'claude-3-sonnet':
                model = 'claude-3-sonnet-20240229'
            if model == 'claude-3-haiku':
                model = 'claude-3-haiku-20240307'
            data = json.load(file)
            data['model'] = model
            await ctx.send(f'Changed model to {model}')
            await ctx.bot.change_presence(activity=discord.CustomActivity(name = f'Using {model}'))
            with open('config.json', 'w') as file:
                json.dump(data, file)
        else:
            await ctx.send(f'Check spelling, no such model: {model}')
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
    msg = []
    last_role = None
    for each in kwargs['context']:
        current_role = 'assistant' if each[0] == str(kwargs['ctx'].me.id) else 'user'
        if last_role == current_role:
            msg = []
            break
        msg.append(
            {'role': current_role, 'content': each[1]}
        )
        last_role = current_role
    try:
        if msg[0]['role'] == 'assistant':
            msg.pop(0)
    except IndexError as e:
        pass
    msg.append({"role": "user", "content": kwargs['prompt']})
    claudeClient = AsyncAnthropic(api_key=DiscordToken.claude())
    stream = await claudeClient.messages.create(
        model = kwargs['model'],
        max_tokens = 4096,
        system = kwargs['system'],
        messages = msg,
        stream = False
    )
    return stream
#----------------------------------------------------------------------------------------------------------
async def compileOllamaPost(**kwargs):
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
async def getModelStatus():
    try:
        with open('config.json', 'r') as file:
            data = json.load(file) 
        return data['model']
    except:
        print('No config.json found')
        return