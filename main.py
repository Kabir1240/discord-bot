import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='UTF-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
selected_role = "ping me"
# Handling Events


@bot.event
async def on_ready():
    print(f"We are ready to go in, {bot.user.name}")


@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server {member.name}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if "soap" in message.content.lower():
        await message.delete()
        # .mention will @ them
        await message.channel.send(f"{message.author.mention} fuck you, you can't say that, only I can say soap")

    # this line is really important, and you should always add it at the end
    await bot.process_commands(message)


# this is to talk to the bot directly, instead of handling an event
@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")


@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=selected_role)
    if role:
        await ctx.author.add_roles(role)
        print(role)
        await ctx.send(f"{ctx.author.mention} is now assigned to {selected_role}")
    else:
        await ctx.send(f"Couldn't find {selected_role}")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)
