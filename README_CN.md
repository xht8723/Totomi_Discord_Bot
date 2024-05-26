# TotomiBot 远江bot
[English](/README.md)  
  
一个能够使用大型语言模型LLM的Dsicord机器人！（包括chatgpt，claude3或者本地运行的ollama）
  
![image](https://github.com/xht8723/Totomi_Discord_Bot/assets/15156436/8e39753e-286c-4dc3-b6a7-39469dabf905)
![image](https://github.com/xht8723/Totomi_Discord_Bot/assets/15156436/6fad4881-f41a-4d91-bc9b-363385fcb1cc)
基于[discord.py](https://github.com/Rapptz/discord.py)  
你需要有自己的llm api  

## Dependencies 需求python模组
```pip install discord.py```  
```pip install requests```  
```pip install openai```  

## 使用
下载这个repo并解压  
安装上述前置模组  
替换所有```DiscordToken.totomiT()```代码为你的discord机器人token（有一个替换在```run.py```里, 有一个替换在```run_win.pyw```里）  
替换所有```DiscordToken.openAI()```代码为你的openAI api. （有一个需替换，在```commands.py```里）  
运行```python run.py```  

或者双击使用windows版```run_win.pyw```  
