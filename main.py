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
    user_roles = ctx.author.roles
    for user_role in user_roles:
        if user_role.name == selected_role:
            await ctx.send(f"{ctx.author.mention} is already assigned to {selected_role}")
            return

    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is now assigned to {selected_role}")
    else:
        await ctx.send(f"Couldn't find {selected_role}")


@bot.command()
async def unassign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=selected_role)
    if role:
        user_roles = ctx.author.roles
        for user_role in user_roles:
            if user_role.name == selected_role:
                await ctx.author.remove_roles(role)
                await ctx.send(f"{selected_role} is now removed from {ctx.author.mention}")
                return
        await ctx.send(f"{ctx.author.mention} doesn't have the {selected_role}")
    else:
        await ctx.send(f"Couldn't find {selected_role}")


@bot.command()
@commands.has_role(selected_role)
async def secret(ctx):
    await ctx.send("Welcome to the club!")


@secret.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("you do not have permission to do that!")


@bot.command()
async def dm(ctx, *, msg):
    await ctx.author.send(f"You said {msg}")


@bot.command()
async def reply(ctx):
    await ctx.reply("This is a reply to your message")


@dm.error
async def dm_error(ctx, error):
    print(error)


@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="polling", description=question)
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")


bot.run(token, log_handler=handler, log_level=logging.DEBUG)
