# TotomiBot
[中文](/README_CN.md)  
  
A discord bot that utilized popular LLMs inlcuding chatgpt  
  
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

### todos:  
status commands
model settings individually
more SQL
logs  
send picture  
excute commands use natural languages.  
more LLMs  
context for ollama  
make this a COG  

### Ultimate goal: Chat with gpt-4o in voice channel!

### knwon bugs:
windows tray cannot close gracefully.
