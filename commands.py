from openai import AsyncOpenAI
from openai import OpenAI
from anthropic import AsyncAnthropic
import requests
import json
from discord.ext import commands
from discord import app_commands
import utilities as ut
import discord
import base64
import os
import asyncio

#-------------------------------------------------------------
# commands
# This is a module for every main discord commands.
#-------------------------------------------------------------

SQL = 'chat_history.db'#SQL data base location.
CONFIG = 'config.json'#config.json location.

# Usable AI models.
MODELS = ['gpt-3.5-turbo', 'gpt-4o', 'gpt-4-turbo', 'ollama', 'claude-3-opus', 'claude-3-sonnet', 'claude-3-haiku']
# Usable AI models that supports vision(to read a picture.)
VISION_MODELS = ['gpt-4o', 'gpt-4-turbo', 'claude-3-opus-20240229', 'claude-3-sonnet-20240229', 'claude-3-haiku-20240307']
# Usable AI models that generate images.
ART_MODELS = []

#-------------------------------------------------------------
# newchat
# This is a discord command to clear current chat context.
#-------------------------------------------------------------
@commands.hybrid_command(description = 'clear context, start a new chat.')
async def newchat(ctx):
    ut.logRequest(ctx)
    ctx.bot.NEWCHAT = 1
    await ctx.send('Cleared context!')
    return

#-------------------------------------------------------------
# totomi
# This is a discord command to chat with AI
#-------------------------------------------------------------
@commands.hybrid_command(description="start chat!", help = 'say something')
async def totomi(ctx, prompt: str):
    ut.logRequest(ctx, prompt)
    await ctx.defer()

    with open(CONFIG, 'r') as file:
        data = json.load(file)

    systemP = data['systemPrompt']
    model = data['model']
    normalModeContextLength = data['normalModeContextLength']
    threadModeContextLength = data['threadModeContextLength']

    OPENAI_API = data['openAI-api']
    CLAUDE3_API = data['claude3-api']

    if ctx.guild == None:
        guild = 'DM'
    else:
        guild = str(ctx.guild.id)

    prompt = 'From user ' + f'<@{str(ctx.author.id)}>: ' + prompt 

    if ctx.bot.NEWCHAT == 1:
        context = []
        ctx.bot.NEWCHAT = 0
    else:
        context = ut.get_latest_guild_messages(str(ctx.channel.id), guild, normalModeContextLength)

    if model == 'ollama':
        try:
            url = 'http://localhost:11434/api/chat'
            data = ollamaPost(prompt=prompt, system = systemP)
            post = requests.post(url, json=data)
            jsondata = post.json()
            await ctx.send(jsondata['message']['content'])
        except Exception as e:
            await ctx.send(str(e))

    if model == 'gpt-3.5-turbo' or model == 'gpt-4o' or model == 'gpt-4-turbo':
        try:
            data = await chatGPTPOST(prompt = prompt, system = systemP, 
                                     model = model, context = context, ctx = ctx, 
                                     img = None, attachment = None, api = OPENAI_API)
            reply = data.choices[0].message.content + '\n\n' + '*token spent: ' + str(data.usage.total_tokens) + '*'
            reply_raw = data.choices[0].message.content
            await ctx.send(reply)

            ut.save_guild_message(str(ctx.channel.id), guild, str(ctx.author.id), prompt)
            ut.save_guild_message(str(ctx.channel.id), guild, str(ctx.me.id), data.choices[0].message.content)
        except Exception as e:
            await ctx.send(str(e))
    
    if model == 'claude-3-opus-20240229' or model == 'claude-3-sonnet-20240229' or model == 'claude-3-haiku-20240307':
        try:
            data = await claudePOST(prompt = prompt, system = systemP, 
                                     model = model, context = context, ctx = ctx, 
                                     img = None, attachment = None, api = CLAUDE3_API)
            reply = data.content[0].text + '\n\n' + '*token spent: ' + str(data.usage.input_tokens + data.usage.output_tokens) + '*'
            reply_raw = data.content[0].text
            await ctx.send(reply)

            ut.save_guild_message(str(ctx.channel.id), guild, str(ctx.author.id), prompt)
            ut.save_guild_message(str(ctx.channel.id), guild, str(ctx.me.id), data.content[0].text)
        except Exception as e:
            await ctx.send(str(e))
    return reply_raw

#-------------------------------------------------------------
# imgtotomi
# This is a discord command to ask vision AI about an image.
#-------------------------------------------------------------
@commands.hybrid_command(description = 'ask AI about an image')
@app_commands.describe(prompt = 'ask something', image = 'drag your image here')
async def imgtotomi(ctx, prompt: str, image: discord.Attachment):
    ut.logRequest(ctx, prompt + ' file: ' + image.filename)

    with open(CONFIG, 'r') as file:
        data = json.load(file)

    _, fileExtension = os.path.splitext(image.filename)
    fileExtension = fileExtension[1:]
    if fileExtension == 'jpg':
        fileExtension = 'jpeg'
    systemP = data['systemPrompt']
    model = data['model']
    OPENAI_API = data['openAI-api']
    CLAUDE3_API = data['claude3-api']

    if model not in VISION_MODELS:
        await ctx.send(f'Current AI model does not have vision capability.\nVision supported models: {VISION_MODELS}')
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
    imgDataUrl = f"data:image/{fileExtension};base64,{b64img}"

    if model == 'gpt-4o' or model == 'gpt-4-turbo':
        data = await chatGPTPOST(prompt = prompt, system = systemP, 
                                model = model, context = None, ctx = ctx, 
                                img = imgDataUrl, attachment = None, fileExtension = fileExtension, api = OPENAI_API)
        reply = data.choices[0].message.content + '\n\n' + '*token spent: ' + str(data.usage.total_tokens) + '*'
        await ctx.send(reply)
        ut.save_guild_message(str(ctx.channel.id), guild, str(ctx.author.id), prompt + 'uploaded img: ' + str(image.id))
        ut.save_guild_message(str(ctx.channel.id), guild, str(ctx.me.id), data.choices[0].message.content)

    if model == 'claude-3-opus-20240229' or model == 'claude-3-sonnet-20240229' or model == 'claude-3-haiku-20240307':
        data = await claudePOST(prompt = prompt, system = systemP, 
                                model = model, context = None, ctx = ctx, 
                                img = b64img, attachment = None, fileExtension = fileExtension, api = CLAUDE3_API)
        reply = data.content[0].text + '\n\n' + '*token spent: ' + str(data.usage.input_tokens + data.usage.output_tokens) + '*'
        await ctx.send(reply)
        ut.save_guild_message(str(ctx.channel.id), guild, str(ctx.author.id), prompt + 'uploaded img: ' + str(image.id))
        ut.save_guild_message(str(ctx.channel.id), guild, str(ctx.me.id), data.content[0].text)

#-------------------------------------------------------------
# dalle_totomi
# This is a discord command to use openAI's DALL-E-3 to generate images.
#-------------------------------------------------------------
@commands.hybrid_command(description = 'Image Generation')
@app_commands.describe(prompt = 'Describe your image!', style = 'vivid/natural', 
                       size = 'must be 1024x1024, 1792x1024 or 1024x1792',
                       quality = 'standard/hd')
async def dalle_totomi(ctx, prompt: str, style:str = 'vivid', size:str = '1024x1024', quality:str = 'hd'):
    ut.logRequest(ctx, prompt)
    with open(CONFIG, 'r') as f:
        data = json.load(f)

    OPENAI_API = data['openAI-api']
    openaiClient = AsyncOpenAI(api_key=OPENAI_API)
    await ctx.defer()
    try:
        response = await openaiClient.images.generate(
            model='dall-e-3',
            prompt=prompt,
            style=style,
            size=size,
            quality=quality
        )
    except Exception as e:
        await ctx.send(e)
    reply = ''
    for each in response.data:
        reply = reply + each.url + '\n'
    await ctx.send(reply)
    return

#-------------------------------------------------------------
# ttstotomi
# This is a discord command to make AI speak to you.
#-------------------------------------------------------------
@commands.hybrid_command(description = 'Simple text to speech.')
@app_commands.describe(prompt = 'Chat', voice = 'alloy/echo/fable/onyx/nova/shimmer', model = 'tts-1/tts-1-hd')
async def tts(ctx, prompt: str, voice: str = 'nova', model: str = 'tts-1'):
    ut.logRequest(ctx, prompt + ',' + voice + ',' + model)
    if ctx.author.voice.channel == None:
        ctx.send('You have to be in a voice channel.')
        return
    with open(CONFIG, 'r') as f:
        data = json.load(f)
    OPENAI_API = data['openAI-api']
    openaiClient = OpenAI(api_key=OPENAI_API)
    try:
        with openaiClient.with_streaming_response.audio.speech.create(model=model,voice=voice,input=prompt) as response:
            response.stream_to_file('tts.mp3')
    except Exception as e:
        await ctx.send(e)
    audio = discord.FFmpegPCMAudio(
            source='tts.mp3'
        )
    channel = ctx.author.voice.channel
    if channel is not None and ctx.voice_client is None:
        voice_client = await channel.connect()
    else:
        voice_client = ctx.voice_client
    voice_client.play(audio, after=lambda _:asyncio.run_coroutine_threadsafe(
            coro = voice_client.disconnect(),
            loop = voice_client.loop
        ).result())
    ctx.send('TTS done.')
    
#-------------------------------------------------------------
# ttstotomi
# This is a discord command to voice chat with AI
#-------------------------------------------------------------
@commands.hybrid_command(description = 'AI speaks to you, literally.')
@app_commands.describe(prompt = 'Chat', voice = 'alloy/echo/fable/onyx/nova/shimmer', model = 'tts-1/tts-1-hd')
async def ttstotomi(ctx, prompt: str, voice: str = 'nova', model: str = 'tts-1'):
    reply = await ctx.invoke(totomi, prompt)
    await ctx.invoke(tts, prompt=reply, voice = voice, model = model)
    return
#-------------------------------------------------------------
# usemodel
# This is a discord command to change AI models.
#-------------------------------------------------------------
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
            json.dump(data, file, indent = '\t', ensure_ascii=False)
    else:
        await ctx.send(f'Check spelling, available models: *gpt-3.5-turbo, gpt-4o, gpt-4-turbo, ollama, claude-3-opus, claude-3-sonnet, claude-3-haiku*')
    return

#-------------------------------------------------------------
# help
# This is a discord command to show help text. It will use the descriptions in config.json
#-------------------------------------------------------------
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
#-------------------------------------------------------------
# set_context_length
# This is a discord command to set context length for AI chat.
#-------------------------------------------------------------
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

#-------------------------------------------------------------
# check_model
# This is a discord command to show currently using AI model.
#-------------------------------------------------------------
@commands.hybrid_command(description = 'check current model')
async def check_model(ctx):
    ut.logRequest(ctx)
    with open(CONFIG, 'r') as file:
        data = json.load(file)
    model = '**' + data['model'] + '**'
    await ctx.send(f'Currently using LLM: {model}')
    await ctx.send('All available models: *gpt-3.5-turbo, gpt-4o, gpt-4-turbo, ollama, claude-3-opus, claude-3-sonnet, claude-3-haiku*')

#-------------------------------------------------------------
# set_system_prompt
# This is a discord command to set system prompt for AI chat.
#-------------------------------------------------------------
@commands.hybrid_command(description = 'Set system prompt.')
@app_commands.describe(prompt = 'Enter new system prompt')
async def set_system_prompt(ctx, prompt:str):
    ut.logRequest(ctx, prompt)
    if not ut.isAdmin(str(ctx.author.id)):
        await ctx.send('You don\'t have the authorization to set system prompt')
        return
    with open(CONFIG,'r') as file:
        data = json.load(file)
    data['systemPrompt'] = prompt
    await ctx.send(f'Changed system prompt to: {prompt}')
    with open(CONFIG, 'w') as file:
        json.dump(data, file, indent = '\t', ensure_ascii=False)
    return

#-------------------------------------------------------------
#HELPERS
#-------------------------------------------------------------
#-------------------------------------------------------------
# chatGPTPOST
# This is a helper function to compile POST message to chatpgts.
#-------------------------------------------------------------
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
    
    openaiClient = AsyncOpenAI(api_key=kwargs['api'])
    try:
        response = await openaiClient.chat.completions.create(
            model=kwargs['model'],
            messages = msg,
            stream=False
        )
    except Exception as e:
        return e
    return response

#-------------------------------------------------------------
# claudePOST
# This is a helper function to compile POST message to claude3s.
#-------------------------------------------------------------
async def claudePOST(**kwargs):
    msg = []
    if kwargs['img'] == None and kwargs['attachment'] == None:
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

    elif kwargs['attachment'] == None:
        content = []
        extension = kwargs['fileExtension']
        content.append({'type':'image', 'source':{
            'type':'base64',
            'media_type': f'image/{extension}',
            'data':kwargs['img']
        }})
        msg.append({'role':'user', 'content':content})
    else:
        pass
    
    claudeClient = AsyncAnthropic(api_key=kwargs['api'])
    stream = await claudeClient.messages.create(
        model = kwargs['model'],
        max_tokens = 4096,
        system = kwargs['system'],
        messages = msg,
        stream = False
    )
    return stream

#-------------------------------------------------------------
# ollamaPost
# This is a helper function to compile POST message to ollama.
#-------------------------------------------------------------
async def ollamaPost(**kwargs):
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

#-------------------------------------------------------------
# getModelStatus
# This is a helper function that returns currently using AI model.
#-------------------------------------------------------------
async def getModelStatus():
    try:
        with open(CONFIG, 'r') as file:
            data = json.load(file) 
        return data['model']
    except:
        print('No config.json found')
        return

#-------------------------------------------------------------
# encode_image
# This is a helper function for encoding images in base64 so that vision AIs could read them.
#-------------------------------------------------------------
async def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')