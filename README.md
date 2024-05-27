# TotomiBot
[中文](/README_CN.md)  
  
Have the power of LLMs in your discord bot!  
Supported LLMs: chatgpt, claude3, ollama  
  
![image](https://github.com/xht8723/Totomi_Discord_Bot/assets/15156436/8e39753e-286c-4dc3-b6a7-39469dabf905)
![image](https://github.com/xht8723/Totomi_Discord_Bot/assets/15156436/6fad4881-f41a-4d91-bc9b-363385fcb1cc)
Based on [discord.py](https://github.com/Rapptz/discord.py)

## Dependencies
```pip install discord.py```  
```pip install requests```  
```pip install openai```  

## Use
download the repo and unzip to your prefered location  
install above dependencies  
replace all ```DiscordToken.totomiT()``` with your discord bot token. (one in ```run.py```, one in ```run_win.pyw```)  
replace all ```DiscordToken.openAI()``` with your openAI api key. (one in ```commands.py```)  
run ```python run.py```  
  
or for windows tray version double click ```run_win.pyw```  


## Config
After the first running, ```config.json``` and ```chat_history.db``` will be generated in folder.
You can change somesettings in config.json on the fly.  
```systemPrompt```change system prompt for AIs.  
```model```change the AI service, admin users can change this using discord command as well.  
```normalModeContextLength``` change the context length for your conversations. 5 means the AI will remember your past 5 conversations. -1 means unlimited.  
```threadModeContextLength``` same as above, but used in a discord thread.(thread not yet implemented.)  
```admins``` is an array of admin users id. only admins can use discord commands to change certain settings.  
```commands``` this is used to show ```/help``` texts. You can modify them in the description part.

### todos:  
discord threads
logs  
send picture  
excute commands use natural languages.  
context for ollama  
make this a COG  

### Ultimate goal: Chat with gpt-4o in voice channel!

### knwon bugs:
windows tray cannot close gracefully.
