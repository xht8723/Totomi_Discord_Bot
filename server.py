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
        self.NEWCHAT = 1

    async def stop(self):
        await self.close()
    
    async def on_ready(self):
        if not ut.checkSQL():
            ut.initSQL()
        if not ut.checkJson():
            ut.initJson()

        model = await cmds.getModelStatus()
        await self.change_presence(activity=discord.CustomActivity(name = f'Using {model}'))

        try:
            await self.tree.sync()
            print("Commands synced successfully.")
        except Exception as e:
            print(f"Failed to sync commands: {e}")

        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')