import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
ROLE = os.getenv("ROLE")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

player_list = []
queue = []

def get_spots():
    spots = ""
    for i in range(len(player_list)):
        spots += "✅ "

    for i in range(5 - len(player_list)):
        spots += "⬜ "

    return spots

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_reaction_add(reaction, user):
    # if user.name not in player_list:
    if len(player_list) < 5:
        player_list.append(user.name)
        await reaction.message.channel.send(f"{user.display_name} joined the team!\n"
                                            f"Current spots: {get_spots()}")
    else:
        queue.append(user.name)
        await reaction.message.channel.send(f"{user.display_name} was addded to the queue.")


@bot.command()
async def start(ctx, time="right now"):
    if time != "right now":
        time = "at " + time

    role = discord.utils.get(ctx.guild.roles, name=ROLE)
    allowed = discord.AllowedMentions(roles=True)

    player_list.append(ctx.author.name)

    await ctx.send(f"{role.mention} {ctx.author.display_name} wants to play Valorant {time}!\n "
                   f"React to this message in order to reserve your spot in the 5-stack!\n"
                   f"Current spots: {get_spots()}",
                   allowed_mentions=allowed)

@bot.command()
async def list_players(ctx):
    await ctx.send(f"Current players in team: {player_list}")

@bot.command()
async def remove_me(ctx):
    if ctx.author.name in queue:
        queue.remove(ctx.author.name)
        await ctx.send(f"{ctx.author.display_name} has been removed from the queue")

    elif ctx.author.name in player_list:
        player_list.remove(ctx.author.name)
        await ctx.send(f"{ctx.author.display_name} has been removed from the team")

        if len(queue) > 0:
            new_player = queue.pop(0)
            player_list.append(new_player)
            await ctx.send(f"{new_player} has been added to the team!")

    else:
        await ctx.send(f"You are not in the player list or queue.")


bot.run(TOKEN)