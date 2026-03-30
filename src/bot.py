import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import datetime

load_dotenv()
TOKEN = os.getenv("TOKEN")
ROLE = os.getenv("ROLE")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

player_list = []
queue = []

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_reaction_add(reaction, user):
    # if user.name not in player_list:
    player_list.append(user.name)
    await reaction.message.channel.send(f"{user.display_name} joined the team!")

@bot.command()
async def start(ctx, time="right now"):
    if time != "right now":
        time = "at " + time

    role = discord.utils.get(ctx.guild.roles, name=ROLE)
    allowed = discord.AllowedMentions(roles=True)

    player_list.append(ctx.author.name)

    await ctx.send(f"{role.mention} {ctx.author.display_name} wants to play Valorant {time}!\n "
                   f"React to this message in order to reserve your spot in the 5-stack!\n"
                   f"Current spots: ✅ ⬜ ⬜ ⬜ ⬜", allowed_mentions=allowed)

@bot.command()
async def list_players(ctx):
    await ctx.send(f"Current players in team: {player_list}")

bot.run(TOKEN)