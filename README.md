# TotomiBot
Master version is for Ubuntu machine, checkout windows branch for windows machine.


A basic discord bot, for anyone who want your own free music bot service in your discord channel. As, other bots clearly suffers from music quality issues due to server overload.
You need your own server. Or could just run on your PC.



Check out commands by typing `-help` in discord.
command and prefix can be personalized in json file.



## **How to use:**

1.Install node.js, search for how to install as it depands on different operating systems. **Though this master version is for Ubuntu. Checkout windows branch if you are using windows VM**

2.Apply for discord API services, and create a bot identity in https://discord.com/developers/applications. Copy the token.

3.Download `index.js` and `config.json` from here. Open `config.json` with txt editor, paste the token after "token" line.

4.Direct your console to the file folder contains `index.js` and `config.json`. Type ```npm i totomi_bot``` to install the packages needed.

5.Run bot with `node index.js` in console.

6.In discord application page, in OAuth2 tab, check "bot", scroll down, check "Send messages", "View Channels", "Connect", "Speak". Now you have your bot invitation link displayed above. Invite your bot into your channel.




## 中文
Master branch是给Ubuntu机器用的，如果你是Windows，请查看Windows branch.

一个基础的免费音乐bot，可以在discord语音频道中播放youtube视频。
你需要一个自己的服务器，或者在你电脑上运行也行。

在discord里打-help查看指令。
指令等可以在config.json文件中自定义。

### 如何使用

1.安装node.js，善用搜索。**注意Master branch是给ubuntu机器的，windows版在windows branch里。**

2.申请discord API服务，并建立一个bot：https://discord.com/developers/applications 复制bot下面的token

3.用console cd到想要的文件夹，使用```npm i totomi_bot```来安装packages.

4.把这个repo的`index.js`以及`config.json`复制到那个文件夹里，并打开`config.json`，在其中`token`那一栏里，把你上面拿到的discord token复制进去。

5.在console输入`node index.js`，运行bot.

5.在上面的discord application页面，打开OAuth2，把里面的Bot打勾，然后再把下面的"Send messages", "View Channels", "Connect", "Speak"打勾。然后在上面你就会得到一个邀请链接。你现在可以邀请你的bot进入你的频道了。
