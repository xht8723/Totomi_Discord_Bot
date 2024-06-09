import logging.handlers
import aioconsole
from discord.ext import commands
import commands as cmds
import utilities as ut
from youPlay_cog import YTDL
import discord
import logging
from utilities import add_admin, set_claude_key, set_openai_key, set_sys_prompt, set_model, set_context_len

#-------------------------------------------------------------
# server
# This is the main module for running the bot server.
#-------------------------------------------------------------

# these are terminal commands.
imported_functions = {
    'add_admin': add_admin,
    'set_claude_key':set_claude_key,
    'set_openai_key':set_openai_key,
    'set_sys_prompt':set_sys_prompt,
    'set_model':set_model,
    'set_context_len':set_context_len
}

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log',encoding='utf-8')
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)
logger.addHandler(handler)
logging.getLogger('discord.http').setLevel(logging.INFO)

#-------------------------------------------------------------
# command_listener
# This is a coroutine that will run along with the server to listen to terminal commands.
#-------------------------------------------------------------
async def command_listener():
    while True:
        try:
            IOin = await aioconsole.ainput('>> ')
            inputToken = IOin.split()
            if not inputToken:
                continue
            cmd = inputToken[0]
            args = inputToken[1:]

            if cmd == 'exit':
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
            logging.error(e)

#-------------------------------------------------------------
# help
# This is a terminal commands to show help text for terminal commands.
#-------------------------------------------------------------
def help():
    print('------terminal commands------')
    for key in imported_functions:
        print(key)
    print('--------usage: <invoke command_name args>--------')
    return

#-------------------------------------------------------------
# Totomi
# This is the main class of the bot server.
#-------------------------------------------------------------
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
        self.add_command(cmds.tts)
        self.add_command(cmds.ttstotomi)
        self.NEWCHAT = 1

    #-------------------------------------------------------------
    # setup_hook
    # This will get called after on_ready.
    # Used to create coroutine for listening to terminal commands.
    #-------------------------------------------------------------
    async def setup_hook(self) -> None:
        self.commandListener = self.loop.create_task(command_listener())
    
    #-------------------------------------------------------------
    # on_ready
    # This will get called when the bot is ready.
    # Used to setup SQL databse, setting up discord presence, sync discord slash commands.
    #-------------------------------------------------------------
    async def on_ready(self):
        await self.add_cog(YTDL(self))
        if not ut.checkSQL():
            print('init SQL....')
            ut.initSQL()

        await self.change_presence(activity=discord.CustomActivity(name = f'/help'))

        try:
            await self.tree.sync()
            print("Commands synced successfully.")
        except Exception as e:
            logging.error(e)
            print(f"Failed to sync commands: {e}")

        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('\nThank you for using totomi bot!\nsome configs are in config.json file.\n')
        print('------input <invoke help> to see available terminal commands')


#-------------------------------------------------------------
# Server preparations
#-------------------------------------------------------------
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
if not ut.checkJson():
    token = input('Enter discord token: ')
    openAi = input('Enter openAI api key\n(can leave it blank and change it later in json file): ')
    claude3 = input('Enter claude3 api key\n(can leave it blank and change it later in json file): ')
    admin = input('Enter the admin user\'s discord ID: ')
    client = Totomi(command_prefix='!', intents=intents, help_command=None, openAi = openAi, claude3 = claude3, token = token, admin = admin)
    ut.initJson(token, claude3, openAi, admin)
else:
    client = Totomi(command_prefix='!', intents=intents, help_command=None)
keys = ut.getAPIs()

#-------------------------------------------------------------
# python main to start server.
#-------------------------------------------------------------
if __name__ == '__main__':
    client.run(keys['token'], log_handler=None)
