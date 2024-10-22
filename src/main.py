import discord
from discord.ext import commands
import json
import random
import asyncio
from colorama import Fore, Style, init

init(autoreset=True)

with open('config.json', 'r') as among_us_imspta_sussy:
    config = json.load(among_us_imspta_sussy)

prefix = config["prefix"]
token = config["token"]
delay = config.get("delay", 0.1)
ratelp = config.get("rate_limit_pause", 5.0)

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
        users = random.sample(ctx.guild.members, min(69, len(ctx.guild.members))) if len(ctx.guild.members) > 0 else []
        p_msg = " 🗿 ".join([user.mention for user in users])

        try:
            msg = await ctx.send(p_msg)
            await asyncio.sleep(delay)

            try:
                await msg.delete()
            except discord.HTTPException:
                pass

        except discord.HTTPException as error:
            if error.status == 50013:
                print(f"{Fore.RED} [!] You Got Muted LLL :sob:")
                exit(50013)
            elif error.status == 50001:
                print(f"{Fore.RED}[!] You Got Muted!")
                exit(50001)
            elif error.status == 200000:
                print(f"{Fore.RED} [!] This can't be posted because it exceeds the mention limit set by this server. This may also be viewed by server owners \n -Discord")
                exit(200000)
            elif error.status == 429:
                af = int(error.headers.get("Retry-After", ratelp))
                print(f"{Fore.RED} [!] Rate Limited! Pausing for {af} seconds...")
                await asyncio.sleep(af)
                continue
            else:
                print(f"{Fore.RED}[!] Pinging Error!: {error}")
                print(f"{Fore.RED} [!] Unknown Error!")

        await asyncio.sleep(delay)

@bot.command()
async def stop(ctx):
    global isp
    isp = False
    await ctx.message.delete()

bot.run(token)
