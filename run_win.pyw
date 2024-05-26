import pystray
from PIL import Image
import threading
import server
import discord
import DiscordToken#delete this or create your own token env

def on_clicked(icon, item):
    if str(item) == "Exit":
        icon.stop()

def run_script():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.guilds = True
    client = server.Totomi(command_prefix='_', intents=intents, help_command=None)
    client.run(DiscordToken.totomiT()) #change to your token value

def main():
    image = Image.open("icon.ico")
    menu = pystray.Menu(pystray.MenuItem("Exit", on_clicked))
    icon = pystray.Icon("Totomi server", image, "Running hard >///<", menu)

    server_thread = threading.Thread(target=run_script)
    server_thread.start()
    icon.run()

if __name__ == "__main__":
    main()