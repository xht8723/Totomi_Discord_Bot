import sqlite3
from datetime import datetime
import os
import json

SQL = 'chat_history.db'
CONFIG = 'config.json'

def checkSQL():
    return os.path.isfile(SQL)

def checkJson():
    return os.path.isfile(CONFIG)

def save_guild_message(channel_id, guild_id, user_id, text):
    sql = sqlite3.connect(SQL)
    c = sql.cursor()
    created_at = datetime.now().isoformat()
    c.execute('INSERT INTO message (channel_id, guild_id, user_id, text, created_at) VALUES (?, ?, ?, ?, ?)',
              (channel_id, guild_id, user_id, text, created_at))
    sql.commit()
    return 1

def get_latest_guild_messages(channel_id, guild_id, context_len):
    sql = sqlite3.connect(SQL)
    c = sql.cursor()
    query = '''
    SELECT user_id, text, created_at 
    FROM message 
    WHERE channel_id = ? AND guild_id = ? 
    ORDER BY created_at DESC
    '''
    if context_len != -1:
        query += ' LIMIT ?'
        c.execute(query, (channel_id, guild_id, context_len))
    else:
        c.execute(query, (channel_id, guild_id))

    result = c.fetchall()
    sql.close()
    return result

def initSQL():
    sql = sqlite3.connect(SQL)
    c = sql.cursor()
    c.execute('''
CREATE TABLE guild (
    id TEXT PRIMARY KEY,
    name TEXT
);''')
    c.execute('''
CREATE TABLE channel (
    id TEXT PRIMARY KEY,
    guild_id TEXT,
    name TEXT,
    FOREIGN KEY (guild_id) REFERENCES guild(id)
);''')
    c.execute(
'''CREATE TABLE message (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    channel_id TEXT,
    guild_id TEXT,
    user_id TEXT,
    text TEXT,
    created_at TEXT,
    FOREIGN KEY (channel_id) REFERENCES channel(id),
    FOREIGN KEY (guild_id) REFERENCES guild(id)
);''')
    c.execute(
'''CREATE TABLE dm_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    text TEXT,
    created_at TEXT
);''')
    return sql.close()


SYSTEMPROMPT = '''你是一个discord bot，你的名字叫远江, 你是一个女生，说话语气可爱，你会回答用户们的问题并且和用户们聊天。
每次输入的开头中'<@numbers>'即是用户的名字id，每次回复都必须严格按照'<@numbers>'的格式提及用户。
除非用户特别说明，应以用户使用的语言回复。'''
def initJson():
    data = {
        'systemPrompt': SYSTEMPROMPT,
        'model': 'gpt-3.5-turbo',
        'normalModeContextLength':'5',
        'threadModeContextLength':'-1',
        'commands': [
            {'command':'help', 'description':'```/help```Help'},
            {'command':'totomi', 'description':'```/totomi <propmt>```Start chat with Totomi!'},
            {'command':'usemodel', 'description':'```/usemodel <model name>```change LLM model.\nAvailable models: gpt-3.5-turbo, gpt-4o, gpt-4-turbo, ollama'},
            {'command':'set_context_length', 'description':'```/set_context_length <mode> <length>```\"thread\" mode or \"normal\" mode\n Set the context length of your chat.'}
        ]
    }
    with open('config.json', 'w') as file:
        json.dump(data, file)