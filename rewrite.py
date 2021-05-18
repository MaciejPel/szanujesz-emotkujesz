import discord 
import os
import asyncio
from   discord.ext    import commands
from   dotenv         import load_dotenv

#intents
intents = discord.Intents.default()
intents.members = True

#bot config
client = commands.Bot(command_prefix='.', intents=intents)

#get token
load_dotenv()

#management commands
@client.event
async def on_ready():
    print("{0.user}".format(client))
    print('discord.py version: '+discord.__version__)
    await client.change_presence(activity=discord.Streaming(name="PP", url="https://www.twitch.tv/vexler_"))

@client.command(aliases=["u"])
@commands.has_permissions(administrator=True)
async def uszanowanko(ctx):
    channel=ctx.channel
    msgs=[]
    used=[]
    result=[]
    if 'uszanowanko' not in channel.name:
        return
    while True:
        try:    
            msg = await client.wait_for('message', check=lambda msg: msg.content=='.end' or len(msg.raw_mentions)==1)
        except asyncio.TimeoutError:
            print(asyncio.TimeoutError)
        else:
            mention=msg.raw_mentions
            if msg.content=='.end':
                break
            elif len(mention)==1 and mention[0] not in used:
                used.append(mention[0])
                msgs.append(msg.id)
                await msg.add_reaction("👏")
            elif mention[0] in used:
                await client.get_channel(channel.id).send(str(ctx.guild.get_member(msg.author.id).mention)+' Ten zawodnik jest już na liście gdzieś wyżej')
            else:
                print('normal msg')
    for mg in msgs:
        message = await client.get_channel(channel.id).fetch_message(mg)
        if message.reactions[0].emoji=="👏" and message.reactions[0].count>1:
            result.append([message.raw_mentions[0], message.reactions[0].count-1])
    print(result)

@client.command(aliases=["e"])
@commands.has_permissions(administrator=True)
async def exit(ctx):
    await client.close()

@client.command(aliases=["d"])
async def delete(ctx, amount=5):
    await ctx.channel.purge(limit=amount+1)

@client.event
async def on_message(message):
    await client.process_commands(message)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error

client.run(os.getenv('TOKEN'))

# useFull stuff
# print(member.display_name, member.name, member.nick, member.desktop_status, member.raw_status, member.web_status, member.bot, member.activity, member.activities,) membersInfo

# problemy
# Po usunięciu wiadomości przechowywanych w msgs wywali giga fetch error
# Rozpoznawanie wiadomości, czy jest to nomicja czy może zwykła konwersacja
# Ograniczenia intents discorda
# Jak sie pobiera emotki serwerowe (?)