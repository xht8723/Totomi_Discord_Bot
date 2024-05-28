from discord.ext import commands
import commands as cmds
import utilities as ut
import discord

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
        self.NEWCHAT = 1
        if not ut.checkJson():
            print('init json file....')
            ut.initJson(kwargs['token'], kwargs['claude3'], kwargs['openAi'], kwargs['admin'])
        cmds.OPENAI_API = kwargs['openAi']
        cmds.CLAUDE3_API = kwargs['claude3']

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
        print('Thank you for using totomi bot.\nsome configs are in config.json file.')
        print('------')

def main():
    token = input('Enter discord token: ')
    openAi = input('Enter openAI api key\n(can leave it blank and change it later in json file): ')
    claude3 = input('Enter claude3 api key\n(can leave it blank and change it later in json file): ')
    admin = input('Enter the admin user\'s discord ID: ')
    intents = discord.Intents.default()
    intents.message_content = True
    intents.guilds = True
    client = Totomi(command_prefix='-', intents=intents, help_command=None, openAi = openAi, claude3 = claude3, token = token, admin = admin)
    client.run(token) #change to your token value

if __name__ == '__main__':
    main()