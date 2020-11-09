# TotomiBot
Master version is for Ubuntu machine, checkout windows branch for windows machine.


A basic discord bot, for anyone who want your own free music bot service in your discord channel. As, other bots clearly suffers from music quality issues due to server overload.
You need your own server. Or could just run on your PC.



To play youtube songs&add songs to que, in discord voice channel. Command `-p <youtube link>` Leave channel `-l | -L` skip current song: `-skip`.
Dice rolling. Command `-roll <int>`

command and prefix can be personalized in json file.



**How to use:**

1.Install node.js, search for how to install as it depands on different operating systems. **Though this master version is for Ubuntu. Checkout windows branch if you are using windows VM**

2.Apply for discord API services, and create a bot identity in https://discord.com/developers/applications. Copy the token.

3.Download this package and unpack them. Open config.json with txt editor, paste the token after "token" line.

4.Direct your console to the file folder. Type `node index.js` to run it.

5.In discord application page, in OAuth2 tab, check "bot", scroll down, check "Send messages", "View Channels", "Connect", "Speak". Now you have your bot invitation link displayed above. Invite your bot into your channel.

6.Done. Enjoy your own bot.
