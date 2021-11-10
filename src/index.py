import discord
from discord import guild
from discord import client
from discord.activity import Game
from discord.channel import VoiceChannel
from discord.ext import commands
from dotenv import load_dotenv
import os
import youtube_dl

#Control del token
load_dotenv()
Token : str =os.getenv('PYTHON_MUSIC_TOKEN',"No se ha encontrado la variable del token")

bot=commands.Bot(command_prefix='>',description="Bot que pronto estará operativo o no")

#Comandos
@bot.command()
async def plai(ctx,url : str):
    song_there = os.path.isfile("song.mp3")
    try:
        if(song_there):
            os.remove("song.mp3")
    except:
        await ctx.send("Espera a que acabe la canción actual, o usa el comando stop") 
        return     
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
    await voiceChannel.connect()
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl':'/canciones',
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))

#Borrar
@bot.command()
async def play(ctx, nombre:str):
    song_there = os.path.isfile("./canciones/"+nombre+".mp3")
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
    await voiceChannel.connect()
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if song_there:
        voice.play(discord.FFmpegPCMAudio("./canciones/"+nombre+".mp3"))
    else:
        await ctx.send("Cancion inexisitente")


@bot.command()
async def leave(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    await voice.disconnect()


@bot.command()
async def download(ctx,url :str, nombre:str):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl':'/home/xatarra/Documentos/Proyectos_Git/botDiscord/canciones/'+nombre+'.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    song_there = os.path.isfile("./canciones/"+nombre+".mp3")
    if not os.path.isfile(song_there):
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
           ydl.download([url])
           await ctx.send(nombre +" descargada correctamente")
    
@bot.command()
async def comandos(ctx):
   await ctx.send(">play cancion \n >download url nombre \n >leave \n >pause \n >resume \n >stop")

@bot.command()
async def pause(ctx):
    #voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("No puedo pausar lo que no se está reproduciendo")
@bot.command()
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("No puedo resumir lo que no está pausado")
@bot.command()
async def botfist(ctx):    
    await ctx.send(":punch:")    

@bot.command()
async def stop(ctx):
    #voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    try:
        voice.stop()
    except:
        return

#Envento
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Estar activo"))
    print('Bot arrancado correctamente')
    

bot.run(Token)