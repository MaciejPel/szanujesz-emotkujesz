import discord 
from discord.ext import commands, tasks
import os
import asyncio
from dotenv import load_dotenv
from random import choice
from threading import Timer
import time

#intents
intents = discord.Intents.default()
intents.members = True

#bot config
client = commands.Bot(command_prefix='.', intents=intents)

#get token
load_dotenv()

#listy
grupy=['1.1', '1.2', '2.1', '2.2', '3.1', '3.2', '4.1', '4.2']

#management commands
@client.event
async def on_ready():
    print("{0.user}".format(client))
    print('discord.py version: '+discord.__version__)
    await client.change_presence(activity=discord.Streaming(name="PP", url="https://www.twitch.tv/vexler_"))

@client.command(aliases=["u"])
@commands.has_permissions(administrator=True)
async def uszanowanko(ctx, title:str, minutes:float, groups:str='1.1,1.2,2.1,2.2,3.1,3.2,4.1,4.2'):
    groups=groups.split(',')
    users_list = []
    mgs=[]
    result=[]
    await ctx.guild.chunk()
    channel=ctx.channel

    for g in groups:
        if g not in grupy:
            await client.get_channel(channel.id).send('Błąd w grupach')
            return

    if 'uszanowanko' in channel.name:
        for member in channel.members:
            # if member.bot==False:
            users_list.append(member.id)
    else:
        return

    for user in users_list:
        mg=await client.get_channel(channel.id).send((ctx.guild.get_member(user).display_name))
        await mg.add_reaction("👏")
        mgs.append([mg, user])

    time.sleep(minutes*60)
    
    for mg in mgs:
        message = await client.get_channel(channel.id).fetch_message(mg[0].id)
        if message.reactions[0].emoji=="👏" and message.reactions[0].count>1:
            result.append([mg[1], message.reactions[0].count-1])

    if len(result)>0:
        final='```'
        for r in result:
            final+='ar!m up '+str(ctx.guild.get_member(r[0]).mention)+' '+str(r[1])+'\n'
        final+='```'
        await client.get_channel(channel.id).send(final)
    else:
        return

@client.command(aliases=["e"])
@commands.has_permissions(administrator=True)
async def exit(ctx):
    await client.close()

@client.command(aliases=["d"])
async def delete(ctx, amount=5):
    await ctx.channel.purge(limit=amount+1)

client.run(os.getenv('TOKEN'))







# useFull stuff

# print(member.display_name, member.name, member.nick, member.desktop_status, member.raw_status, member.web_status, member.bot, member.activity, member.activities,) membersInfo