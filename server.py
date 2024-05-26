import discord
import DiscordToken #Delete this..
from discord.ext import commands
import commands as cmds
import utilities as ut

#----------------------------------------------------------------------------------------------------------

class Totomi(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_command(cmds.totomi)
        self.add_command(cmds.usemodel)
        self.add_command(cmds.help)
        self.add_command(cmds.set_context_length)

    async def on_ready(self):
        if not ut.checkSQL():
            ut.initSQL()
        if not ut.checkJson():
            ut.initJson()

        try:
            await self.tree.sync()
            print("Commands synced successfully.")
        except Exception as e:
            print(f"Failed to sync commands: {e}")

        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')




#----------------------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------------------
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
client = Totomi(command_prefix='_', intents=intents, help_command=None)
client.run(DiscordToken.totomiT()) #change to your token value
