import sys
import asyncio
from discord.ext import commands
import commands as cmds
import utilities as ut
import youPlay
import discord
import threading
from utilities import add_admin, set_claude_key, set_openai_key, set_sys_prompt, set_model, set_context_len
imported_functions = {
    'add_admin': add_admin,
    'set_claude_key':set_claude_key,
    'set_openai_key':set_openai_key,
    'set_sys_prompt':set_sys_prompt,
    'set_model':set_model,
    'set_context_len':set_context_len
}

stop_event = threading.Event()

class Totomi(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_command(cmds.totomi)
        self.add_command(cmds.usemodel)
        self.add_command(cmds.help)
        self.add_command(cmds.set_context_length)
        self.add_command(cmds.check_model)
        self.add_command(cmds.imgtotomi)
        self.add_command(cmds.newchat)
        self.add_command(cmds.dalle_totomi)
        self.add_command(cmds.set_system_prompt)
        self.add_command(youPlay.play)
        self.NEWCHAT = 1
        if not ut.checkJson:
            print('init json...')
            ut.initJson(kwargs['token'], kwargs['claude3'], kwargs['openAi'], kwargs['admin'])

    async def stop(self):
        await self.close()
    
    async def on_ready(self):
        if not ut.checkSQL():
            print('init SQL....')
            ut.initSQL()

        model = await cmds.getModelStatus()
        await self.change_presence(activity=discord.CustomActivity(name = f'Using {model}'))

        try:
            await self.tree.sync()
            print("Commands synced successfully.")
        except Exception as e:
            print(f"Failed to sync commands: {e}")

        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('\nThank you for using totomi bot!\nsome configs are in config.json file.\n')
        print('------input <invoke help> to see available terminal commands')

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
if not ut.checkJson():
    token = input('Enter discord token: ')
    openAi = input('Enter openAI api key\n(can leave it blank and change it later in json file): ')
    claude3 = input('Enter claude3 api key\n(can leave it blank and change it later in json file): ')
    admin = input('Enter the admin user\'s discord ID: ')
    client = Totomi(command_prefix='_', intents=intents, help_command=None, openAi = openAi, claude3 = claude3, token = token, admin = admin)
else:
    client = Totomi(command_prefix='_', intents=intents, help_command=None)

keys = ut.getAPIs()
async def startServer():
    await client.start(keys['token'])

async def close_bot():
    await client.close()

def command_listener():
    while not stop_event.is_set():
        try:
            IOin = input('>> ')
            inputToken = IOin.split()
            if not inputToken:
                continue
            cmd = inputToken[0]
            args = inputToken[1:]

            if cmd == 'exit':
                stop_event.set()
                raise KeyboardInterrupt
                break
            elif cmd == 'invoke' and len(args) >= 1:
                func = args[0]
                func_para = args[1:]
                if func in globals() and callable(globals()[func]):
                    globals()[func](*func_para)
                elif func in imported_functions and callable(imported_functions[func]):
                    imported_functions[func](*func_para)
                else:
                    print(f'function {func} does not exists.')
            else:
                print('syntax error')

        except Exception as e:
            print('closing..')
            raise KeyboardInterrupt
            
def help():
    print('------terminal commands------')
    for key in imported_functions:
        print(key + 'n')
    print('--------usage: <invoke command_name args>--------')
    return

if __name__ == '__main__':
    try:
        listener = threading.Thread(target=command_listener)
        listener.start()
    except:
        raise KeyboardInterrupt
    client.run(keys['token'])
    listener.join()