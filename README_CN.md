# TotomiBot 远江bot
[English](/README.md)  
  
一个能够使用大型语言模型LLM的Dsicord机器人！（包括chatgpt，claude3或者本地运行的ollama） 

  https://github.com/xht8723/Totomi_Discord_Bot/assets/15156436/2eb809d8-4af8-4af8-bae2-172bb8a74c24  
  
基于[discord.py](https://github.com/Rapptz/discord.py)  
你需要有自己的llm api  

## Dependencies 安装需求
python3  
```pip install -r requirements.txt```  
需要ffmpeg在系统运行环境中。  

## 使用
下载这个repo并解压  
安装上述前置模组  
运行```python3 server.py```  

首次运行会让你输入discord token等信息，只有token是必填的，其它的可以直接enter跳过（之后可以随时在json文件改，或者直接用terminal命令改。）  
  
每一个频道都会有单独的设置（包括私信）  
默认设置为，使用chatgpt-3.5，上下文长度5，和一个默认的system prompt  
请使用discord命令来更改频道的设置。详见```/help```  
  
## 设置
首次运行后，文件夹中将生成 ```config.json``` 和 ```chat_history.db``` 文件。  
```chat_history.db``` 是用于存储聊天记录的数据库。  
  
你可以随时更改 ```config.json``` 中的设置。  
```openAI-api``` 设置openai api key.  
```claude3-api``` 设置claude3 api key.  
```discord-token``` 设置discord token.  
```default_system_prompt``` 更改 AI 的system prompt。（此选项只会更改默认设置没什么用，请用discord命令改设置。） 
```default_model``` 更改 AI 服务，管理员用户也可以使用 Discord 命令来更改此设置。（此选项只会更改默认设置没什么用，请用discord命令改设置。）  
```default_normalModeContextLength``` 更改对话的上下文长度。设置为 5 表示 AI 将记住你过去的 5 次对话。设置为 -1 表示无限制。（此选项只会更改默认设置没什么用，请用discord命令改设置。）  
```admins``` 是管理员用户 ID 的数组。只有管理员才能直接使用 Discord 命令来更改某些设置。  
```commands``` 用于显示 /help 文本。你可以在 description 部分修改它们。  
