import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import datetime

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def start(ctx, time="this time"):
    await ctx.send(f"{ctx.author.mention} wants to play Valorant at {time}!")

bot.run(TOKEN)