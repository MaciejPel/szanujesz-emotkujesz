import discord
import os
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

allowedUsers = []

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
    print('discord.py version: ' + discord.__version__)
    await client.change_presence(activity=discord.Streaming(name="PP", url="https://www.twitch.tv/vexler_"))


@client.command(pass_context=True, aliases=["u"])
async def uszanowanko(ctx, title=''):

    channel = ctx.channel
    msgs = []
    used = []
    result = {}
    pepeyes = discord.utils.find(lambda e: e.name == 'pepeyes', client.emojis)

    if ctx.author.id not in allowedUsers:
        return

    if 'uszanowanko' not in channel.name:
        return

    while True:
        try:
            msg = await client.wait_for('message', check=lambda msg: msg.content == '.end' or len(msg.raw_mentions) == 1)
        except asyncio.TimeoutError:
            print(asyncio.TimeoutError)
        else:
            mention = msg.raw_mentions
            if msg.content == '.end':
                break
            elif len(mention) == 1 and mention[0] not in used:
                member = discord.utils.find(lambda m: m.id == msg.raw_mentions[0], channel.members)
                if member.bot == False:
                    used.append(mention[0])
                    msgs.append(msg.id)
                    await msg.add_reaction(pepeyes)

    for mg in msgs:
        try:
            message = await client.get_channel(channel.id).fetch_message(mg)
        except:
            message = False
        if message:
            for m in message.reactions:
                mention = message.raw_mentions[0]
                if type(m.emoji).__name__ == 'Emoji':
                    if m.emoji.name == 'pepeyes':
                        isBot = discord.utils.find(lambda m: True if (m.id == mention and m.bot == False) else False, channel.members)
                        if isBot:
                            result[mention] = []
                            if message.author.id != mention:
                                result[mention].append(message.author.id)
                            votes = await m.users().flatten()
                            for v in votes:
                                if v.bot == False and m.message.author.id != mention and v.id != message.author.id:
                                    result[mention].append(v.id)

    if len(result) > 0:
        embed = discord.Embed(title=title, color=0x4fde8d)
        embed.set_thumbnail(url="https://emoji.gg/assets/emoji/7529_KEKW.png")
        for r in result:
            if (len(result[r]) > 0):
                embed.add_field(name='ar!member ' + str(ctx.guild.get_member(r).mention) + ' give ' + str(len(result[r]) * 10), value='\u200b', inline=False)
        embed.set_footer(text="Pozdrawiam Pawlaka")
        await client.get_channel(channel.id).send(embed=embed)
    else:
        print('Brak nawiazan')
        return


async def exit(ctx):
    if ctx.author.id not in allowedUsers:
        return
    await client.close()


@client.command(aliases=["c"])
async def clear(ctx, amount=5):
    if ctx.author.id not in allowedUsers:
        return
    await ctx.channel.purge(limit=amount + 1)


@client.event
async def on_message(message):
    await client.process_commands(message)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error


client.run(os.getenv['TOKEN'])

# problemy
# Ograniczenia intents discorda