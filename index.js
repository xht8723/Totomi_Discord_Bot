const Discord = require('discord.js');
const client = new Discord.Client();
const ytdl = require('ytdl-core');
const fs = require('fs');
//const { CommandoClient } = require('discord.js-commando');
const { Structures } = require('discord.js');
const path = require('path');

const que = new Map();

client.once('ready', () => {
	client.user.setActivity('输入-help 食用说明书'); 
});


client.on('message', async message => {
	if(message.content.substring(0, 1) == '-'){
		var args = message.content.substring(1).split(' ');
		var cmd = args[0];
		args = args.splice(1);
		
		switch(cmd){
			case 'p':
				const argsTemp = message.content.split(" ");
				if(!argsTemp[1] || !ytdl.validateURL(argsTemp[1]) ){message.channel.send('Invalid youtube URL'); break;}
				
				const connection = message.member.voice.channel.join().then(
				connection => 
				{
				const dispatcher = connection.play(
				ytdl(argsTemp[1], 
				{quality: "highestaudio"}
				)
				)
				}
				);
				
				break;
			
			case 'l':
				connection = await message.member.voice.channel.leave();
				break;
				
			case 'L':
				connection = await message.member.voice.channel.leave();
				break;
				
			case 'roll':
				const temp = message.content.split(" ");
				if(!temp[1]){message.channel.send('Please indicate range.'); break;}
				
				try{
					message.channel.send(message.member.user.username + ': ' + Math.floor(Math.random() * temp[1]));
				}
				catch(error){
					message.channel.send('Invalid input');
				}
				break;
				
			case 'AV':
				message.channel.send('神秘小链接:kiss:： <https://tinyurl.com/yxn5qoph>');
				break;
			
			case 'av':
				message.channel.send('神秘小链接:kiss:： <https://tinyurl.com/yxn5qoph>');
				break;
			
			case 'help':
				message.channel.send('播放音乐: `-p <youtube链接>` \n离开频道: `-l | -L` \n骰子<范围>: `-roll <int>`\n \n:kiss:成人:kiss:刺激:kiss:好康:kiss:： `-AV`');
				break;
			
		}
		
	}
});

client.login('Nzc0ODI0MTU5MTEyODU1NTc1.X6dZOw.rQuJNYiV9fUeotEjf4l_CF2vFmg');