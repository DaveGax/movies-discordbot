import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from tmdb_api.tmbd_api import get_popular_movies, get_toprated_movies

load_dotenv()
token = os.getenv('token')

intents = discord.Intents.all()
intents.messages = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.command(name='popular')
async def popular(ctx):
    titles = get_popular_movies()
    if titles:
        await ctx.send(f"Popular Movies: {', '.join(titles)}")
    else:
        await ctx.send("Failed to get popular movies.")

@bot.command(name='toprated')
async def toprated(ctx):
    titles = get_toprated_movies()
    if titles:
        await ctx.send(f"Toprated Movies: {', '. join(titles)}")
    else:
        await ctx.send("Failed to get toprated movies.")

@bot.command(name='info')
async def info(ctx):
    await ctx.send('¡Discord bot in development!\nUse "!popular" to see Popular Movies\nUse "!toprated" to see Top Rated Movies')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if 'hi' in message.content.lower():
        await message.channel.send(f'Hi {message.author.name}!')

    await bot.process_commands(message)



bot.run(token)