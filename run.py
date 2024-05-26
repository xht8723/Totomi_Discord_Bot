import discord
import server
import DiscordToken#delete this or create your own token env

#----------------------------------------------------------------------------------------------------------
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
client = server.Totomi(command_prefix='_', intents=intents, help_command=None)
client.run(DiscordToken.totomiT()) #change to your token value
