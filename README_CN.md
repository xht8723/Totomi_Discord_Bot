# TotomiBot 远江bot
[English](/README.md)  
  
一个能够使用大型语言模型LLM的Dsicord机器人！（包括chatgpt，claude3或者本地运行的ollama） 

  https://github.com/xht8723/Totomi_Discord_Bot/assets/15156436/2eb809d8-4af8-4af8-bae2-172bb8a74c24  
  
基于[discord.py](https://github.com/Rapptz/discord.py)  
你需要有自己的llm api  

## Dependencies 需求python模组
```pip install discord.py```  
```pip install requests```  
```pip install openai```  

## 使用
下载这个repo并解压  
安装上述前置模组  
运行```python run.py```  
或者双击使用windows版```run_win.pyw```  

首次运行会让你输入discord token等信息，只有token是必填的，其它的可以直接enter跳过（之后可以随时在json文件改，或者直接用terminal命令改。）

## 设置
首次运行后，文件夹中将生成 ```config.json``` 和 ```chat_history.db``` 文件。  
```chat_history.db``` 是用于存储聊天记录的数据库。  
  
你可以随时更改 ```config.json``` 中的设置。  
```systemPrompt``` 用于更改 AI 的system prompt。  
```model``` 用于更改 AI 服务，管理员用户也可以使用 Discord 命令来更改此设置。  
```normalModeContextLength``` 用于更改对话的上下文长度。设置为 5 表示 AI 将记住你过去的 5 次对话。设置为 -1 表示无限制。  
```threadModeContextLength``` 与上述相同，但用于 Discord thread中。(thread功能尚未实现。)  
```admins``` 是管理员用户 ID 的数组。只有管理员才能直接使用 Discord 命令来更改某些设置。  
```commands``` 用于显示 /help 文本。你可以在 description 部分修改它们。  
