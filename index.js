const config = require('./config.json')
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

async function songQue(message, serverQue){
	const args = message.content.split(" ");
	
	const voiceChannel = message.member.voice.channel;
	if(!voiceChannel){
		return message.channel.send("你不在语音频道。");
	}
	const permissions = voiceChannel.permissionsFor(message.client.user);
	
	if(!permissions.has("CONNECT") || !permissions.has("SPEAK")){
		return message.channel.send("我需要加入以及在语音频道说话的权限。");
	}
	
	const songURL = args[1];
	
	const songInfo = await ytdl.getInfo(args[1],{quality: "highestaudio"});
	
	console.log(songInfo);
	
	const song = {
		title: songInfo.videoDetails.title,
		url: songInfo.url,		
	};
	
	console.log(song.title);
	
	if(!serverQue){
		
		const queContruct = {
		textChannel: message.channel,
		voiceChannel: voiceChannel,
		connection: null,
		songs:[],
		volume: 5,
		playing: true,
		
	};
	
	que.set(message.guild.id, queContruct);
	queContruct.songs.push(song);
	
	var connection = await voiceChannel.join();
	queContruct.connection = connection;
	playMusic(message.guild, queContruct.songs[0]);
	
	}else{
		serverQue.songs.push(song);
		return message.channel.send(`**${song.title}** 已加入歌单。`);
	}
	
}

	function playMusic(guild, song){
		const serverQue = que.get(guild.id);
		if(!song){
			serverQue.voiceChannel.leave();
			que.delete(guild.id);
			return;
		}
		const dispatcher = serverQue.connection.play(ytdl(song.url,{quality: "highestaudio"})).on("finish", () =>  {
			serverQue.songs.shift();
			playMusic(guild, serverQue.songs[0]);
		}).on("error", error => console.error(error));
		
		//dispatcher.setVolumeLogarithmic(serverQue.volume / 5);
		
		serverQue.textChannel.send(`开始播放： **${song.title}**`);
	}
	
	function skip(message, serverQue){
		if(!message.member.voice.channel){
			return message.channel.send("你不在语音频道。");
		}
		
		if(!serverQue){
			return message.channel.send("歌单里没有歌。");
		}
		
		serverQue.connection.dispatcher.end();
	}


client.on('message', async message => {
	if(message.content.substring(0, 1) == config.prefix){
		const serverQue = que.get(message.guild.id);
		
		var args = message.content.substring(1).split(' ');
		var cmd = args[0];
		args = args.splice(1);
		
		switch(cmd){
			case config.cmdPlay:
				const argsTemp = message.content.split(" ");
				if(!argsTemp[1] || !ytdl.validateURL(argsTemp[1]) ){message.channel.send('Invalid youtube URL'); break;}
				songQue(message, serverQue);
				
				
				/*const connection = message.member.voice.channel.join().then(
				connection => 
				{
				const dispatcher = connection.play(
				ytdl(argsTemp[1], 
				{quality: "highestaudio"}
				)
				)
				}
				);*/
				
				break;
			
			case config.cmdAdd:
				
				break;
			
			case config.cmdSkip:
				skip(message, serverQue);
				break;
			
			
			case config.cmdLeave:
				connection = await message.member.voice.channel.leave();
				break;
				
			case config.cmdLeave2:
				connection = await message.member.voice.channel.leave();
				break;
				
			case config.cmdRoll:
				const temp = message.content.split(" ");
				if(!temp[1]){message.channel.send('Please indicate range.'); break;}
				
				try{
					message.channel.send(message.member.user.username + ': ' + Math.floor(Math.random() * temp[1]));
				}
				catch(error){
					message.channel.send('Invalid input');
				}
				break;
				
			case config.cmdAV:
				message.channel.send('神秘小链接:kiss:： <https://tinyurl.com/yxn5qoph>');
				break;
			
			case config.cmdHelp:
				message.channel.send('播放音乐: `-p <youtube链接>` \n离开频道: `-l | -L` \n骰子<范围>: `-roll <int>`\n \n:kiss:成人:kiss:刺激:kiss:好康:kiss:： `-AV`');
				break;
			
		}
		
	}
});

client.login(config.token);