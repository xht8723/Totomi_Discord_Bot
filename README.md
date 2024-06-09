# TotomiBot
[中文](/README_CN.md)  
  
Have the power of LLMs in your discord bot!  
Supported LLMs: chatgpt, claude3, ollama  
  
https://github.com/xht8723/Totomi_Discord_Bot/assets/15156436/2eb809d8-4af8-4af8-bae2-172bb8a74c24  

Based on [discord.py](https://github.com/Rapptz/discord.py)

## Dependencies
```pip install discord.py[voice]```  
```pip install openai```  
```pip install anthropic```  
```pip install yt_dlp```  
```pip install aioconsole```  

have ffmpeg in your path to use youtube play music cog.

## Use
download the repo and unzip to your prefered location  
install above dependencies  
run ```python server.py```  
  
uppon first running, prompt will ask you to input discord token, LLM api keys, admin user.  
only discord token is a must to set the bot up, the others can be omitted.(You can change them on the fly using config.json or terminal commands)  
  
Every text channel will have it's own settings(including DMs)  
Default settings are using chatgpt-3.5, context length 5, and a default system prompt.  
Use discord commands to change them for each different channel. See ```/help```  
  
## Config
Uppon the first running, ```config.json``` and ```chat_history.db``` will be generated in folder.  
```chat_history.db``` is the database for storing chat history.  
  
You can change settings in ```config.json``` on the fly.  
```openAI-api``` set openai api key.  
```claude3-api``` set claude3 api key.  
```discord-token``` set discord token.  
```default_system_prompt``` change system prompt for AIs. (note this only change default settings, use discord command to actually change it.)  
```default_model``` change the AI service, admin users can change this using discord command as well. (note this only change default settings, use discord command to actually change it.)  
```default_normalModeContextLength``` change the context length for your conversations. 5 means the AI will remember your past 5 conversations. -1 means unlimited. (note this only change default settings, use discord command to actually change it.)  
```admins``` is an array of admin users id. only admins can use discord commands to change certain settings.  
```commands``` this is used to show ```/help``` texts. You can modify them in the description part.  

### todos:  
STT   
make this a COG  