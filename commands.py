from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
import requests
import json
import DiscordToken #Delete this..
from discord.ext import commands
from discord import app_commands
import utilities as ut
import discord
import base64
import os

SQL = 'chat_history.db'
CONFIG = 'config.json'
MODELS = ['gpt-3.5-turbo', 'gpt-4o', 'gpt-4-turbo', 'ollama', 'claude-3-opus', 'claude-3-sonnet', 'claude-3-haiku']
VISION_MODELS = ['gpt-4o', 'gpt-4-turbo', 'claude-3-opus', 'claude-3-sonnet', 'claude-3-haiku']

#----------------------------------------------------------------------------------------------------------
@commands.hybrid_command(description="start chat!", help = 'say something')
async def totomi(ctx, *, prompt: str):
    ut.logRequest(ctx, prompt)
    await ctx.defer()

    with open(CONFIG, 'r') as file:
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
                                     model = model, context = context, ctx = ctx, 
                                     img = None, attachment = None)
            reply = data.choices[0].message.content + '\n\n' + '*token spent: ' + str(data.usage.total_tokens) + '*'
            await ctx.send(reply)

            ut.save_guild_message(str(ctx.channel.id), guild, str(ctx.author.id), prompt)
            ut.save_guild_message(str(ctx.channel.id), guild, str(ctx.me.id), data.choices[0].message.content)
        except Exception as e:
            await ctx.send(str(e))
    
    if model == 'claude-3-opus-20240229' or model == 'claude-3-sonnet-20240229' or model == 'claude-3-haiku-20240307':
        try:
            data = await claudePOST(prompt = prompt, system = systemP, 
                                     model = model, context = context, ctx = ctx, 
                                     img = None, attachment = None)
            await ctx.send(data.content[0].text)

            ut.save_guild_message(str(ctx.channel.id), guild, str(ctx.author.id), prompt)
            ut.save_guild_message(str(ctx.channel.id), guild, str(ctx.me.id), data.content[0].text)
        except Exception as e:
            await ctx.send(str(e))
    return
#----------------------------------------------------------------------------------------------------------
@commands.hybrid_command(description = 'ask AI about an image')
@app_commands.describe(prompt = 'ask something', image = 'drag your image here')
async def imgtotomi(ctx, prompt: str, image: discord.Attachment):
    ut.logRequest(ctx, prompt + 'file: ' + image.filename)

    with open(CONFIG, 'r') as file:
        data = json.load(file)

    systemP = data['systemPrompt']
    model = data['model']

    if model not in VISION_MODELS:
        await ctx.send('Current AI model does not have vision capability.')
        return

    if ctx.guild == None:
        guild = 'DM'
    else:
        guild = str(ctx.guild.id)

    prompt = 'From user ' + f'<@{str(ctx.author.id)}>: ' + prompt 

    if ctx.message.attachments:
        attachment = ctx.message.attachments[0]
        image = attachment

    cache = 'cache'
    if not os.path.exists(cache):
        os.makedirs(cache)

    path = os.path.join(cache, str(image.id))
    await ctx.defer()
    await image.save(fp = path)
    b64img = await encode_image(path)
    imgDataUrl = f"data:image/jpeg;base64,{b64img}"

    if model == 'gpt-4o' or model == 'gpt-4-turbo':
        data = await chatGPTPOST(prompt = prompt, system = systemP, 
                                model = model, context = None, ctx = ctx, 
                                img = imgDataUrl, attachment = None)
        reply = data.choices[0].message.content + '\n\n' + '*token spent: ' + str(data.usage.total_tokens) + '*'
        await ctx.send(reply)
        ut.save_guild_message(str(ctx.channel.id), guild, str(ctx.author.id), prompt + 'uploaded img: ' + str(image.id))
        ut.save_guild_message(str(ctx.channel.id), guild, str(ctx.me.id), data.choices[0].message.content)


#----------------------------------------------------------------------------------------------------------
@commands.hybrid_command(description = 'Change AI model.(Require admin)')
@app_commands.describe(model = "gpt-3.5-turbo, gpt-4o, gpt-4-turbo, ollama, claude-3-opus, claude-3-sonnet, claude-3-haiku")
async def usemodel(ctx, model: str):
    ut.logRequest(ctx, model)

    with open(CONFIG,'r') as file:
        data = json.load(file)
    if not ut.isAdmin(str(ctx.author.id)):
        await ctx.send('You don\'t have the authorization to change AI models.')
        return
    if model in MODELS:
        if model == 'claude-3-opus':
            model = 'claude-3-opus-20240229'
        if model == 'claude-3-sonnet':
            model = 'claude-3-sonnet-20240229'
        if model == 'claude-3-haiku':
            model = 'claude-3-haiku-20240307'
        data['model'] = model
        await ctx.send(f'Changed model to {model}')
        await ctx.bot.change_presence(activity=discord.CustomActivity(name = f'Using {model}'))
        with open(CONFIG, 'w') as file:
            json.dump(data, file, indent = '\t')
    else:
        await ctx.send(f'Check spelling, available models: *gpt-3.5-turbo, gpt-4o, gpt-4-turbo, ollama, claude-3-opus, claude-3-sonnet, claude-3-haiku*')
    return
#----------------------------------------------------------------------------------------------------------
@commands.hybrid_command(description="help")
async def help(ctx):
    ut.logRequest(ctx)
    with open(CONFIG, 'r') as file:
        data = json.load(file)
    cmds = data['commands']
    txt = ''
    for each in cmds:
        txt = txt + each['description'] + '\n\n'
    await ctx.send(txt)
    return
#----------------------------------------------------------------------------------------------------------
@commands.hybrid_command(description = 'Change context length.(require admin)', help = 'mode = normal or thread. length = a number.')
@app_commands.describe(mode='Mode of the context (normal/thread)', length='Length of the context')
async def set_context_length(ctx, mode:str, length:str):
    ut.logRequest(ctx, mode + ' ' + length)
    with open(CONFIG, 'r') as file:
        data = json.load(file)
    
    if not ut.isAdmin(str(ctx.author.id)):
        ctx.send('You don\'t have the authorization do set context length.')
        return

    if mode == 'normal':
        data['normalModeContextLength'] = length
        await ctx.send(f'Set Normal mode context length to: {length}')

    if mode == 'thread':
        data['threadModeContextLength'] = length
        await ctx.send(f'Set Normal mode context length to: {length}')
    return
#----------------------------------------------------------------------------------------------------------
@commands.hybrid_command(description = 'check current model')
async def check_model(ctx):
    ut.logRequest(ctx)
    with open(CONFIG, 'r') as file:
        data = json.load(file)
    model = '**' + data['model'] + '**'
    await ctx.send(f'Currently using LLM: {model}')
    await ctx.send('All available models: *gpt-3.5-turbo, gpt-4o, gpt-4-turbo, ollama, claude-3-opus, claude-3-sonnet, claude-3-haiku*')
#----------------------------------------------------------------------------------------------------------
#HELPERS
#----------------------------------------------------------------------------------------------------------
async def chatGPTPOST(**kwargs):
    msg = [
            {'role': 'system', 'content': kwargs['system']}
        ]
    if kwargs['img'] == None and kwargs['attachment'] == None:
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

    elif kwargs['attachment'] == None:
        content = []
        content.append({"type": "text", "text": kwargs['prompt']})
        content.append({'type': 'image_url', 'image_url': {'url': kwargs['img'], 'detail':'auto'}})
        msg.append({'role': 'user', 'content': content})
    else:
        pass

    openaiClient = AsyncOpenAI(api_key=DiscordToken.openAI())
    try:
        response = await openaiClient.chat.completions.create(
            model=kwargs['model'],
            messages = msg,
            stream=False
        )
    except Exception as e:
        return e
    return response
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
        if msg[len(msg)-1]['role'] == 'user':
            msg.pop(len(msg)-1)

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
        with open(CONFIG, 'r') as file:
            data = json.load(file) 
        return data['model']
    except:
        print('No config.json found')
        return

#----------------------------------------------------------------------------------------------------------
async def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')