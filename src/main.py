import discord
from discord.ext import commands
import json
import random
import asyncio
from colorama import Fore, Style, init

init(autoreset=True)


with open('config.json', 'r') as f:
    config = json.load(f)

prefix = config["prefix"]
token = config["token"]
delay = config.get("delay", 0.1)
rate_limit_pause = config.get("rate_limit_pause", 5.0)

bot = commands.Bot(command_prefix=prefix, self_bot=True)

isp = False

@bot.event
async def on_ready():
    print(f"Logged In As {bot.user.name}")
    
    

@bot.command(aliases=['massping', 'pm', 'masping', 'msping'])
async def mp(ctx):
    global isp
    if isp:
        return
    isp = True

    await ctx.message.delete()

    if isinstance(ctx.channel, discord.DMChannel):
        await ctx.send("no L bozo")
        isp = False
        return

    while isp:
        users = random.sample(ctx.guild.members, 69)
        p_msg = " 🗿 ".join([user.mention for user in users])

        try:
            msg = await ctx.send(p_msg)
            await asyncio.sleep(delay)
            await msg.delete()
        except discord.HTTPException as error:
            if error.status == 429:
                print(f" {Fore.RED}[!] Rate limited: {error}. Pausing for {rate_limit_pause} seconds.")
                await asyncio.sleep(rate_limit_pause)
            else:
                print(f"{Fore.RED}[!]Pinging Error!: {error}")

@bot.command()
async def stop(ctx):
    global isp
    isp = False
    await ctx.message.delete()

bot.run(token)
