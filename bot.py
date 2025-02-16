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

bot = commands.Bot(command_prefix='!', intents=intents) #Prefix para usar los comandos '!'

CANAL_PERMITIDO = 1280153631743676448  #Id del canal donde se pueden usar comandos (TESTO)


#Check para verificar que el comando se escriba en el canal permitido
def canal_requerido():
    async def predicate(ctx):
        return ctx.channel.id == CANAL_PERMITIDO
    return commands.check(predicate)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.activity.Game(name='/info'),
                              status=discord.Status.online)
    await bot.tree.sync()
    print(f'{bot.user.name} is logged in.')


#Comando /info para ver la información del bot
@bot.tree.command(name='info', description='See bot information')
async def info(interaction: discord.Interaction):
    embed = discord.Embed(
        title = '__¡Discord bot in development!__',
        color = discord.Color.blue(),
        url = 'https://github.com/DaveGax/movies-discordbot'
    )
    embed.add_field(name = '**Commands**:', value = '!popular <List of popular movies>\n!toprated <List of top rated movies>', inline=False)
    embed.set_footer(text = 'In development by: DaveGax')

    await interaction.response.send_message(embed=embed)


#Comando !popular para ver las peliculas populares
@bot.command(name='popular')
@canal_requerido() #Aplica el check al comando
async def popular(ctx):
    embed = discord.Embed(
        title = '__Popular Movies__',
        color = discord.Color.blue(),
        url = 'https://www.themoviedb.org/movie?language=en'
    )
    titles = get_popular_movies()
    if titles:
        embed.add_field(name='**Movies:**', value='\n'.join(titles), inline=False)
    else:
        embed.add_field(name='**Movies:**', value='Error, movies not found', inline=False)
    
    await ctx.message.delete()
    await ctx.send(embed=embed)


#Comando !toprated para ver las peliculas mejor valoradas
@bot.command(name='toprated')
@canal_requerido() #Aplica el check al comando
async def toprated(ctx):
    embed = discord.Embed(
        title = '__Top Rated Movies__',
        color = discord.Color.blurple(),
        url = 'https://www.themoviedb.org/movie/top-rated?language=en'
    )
    titles = get_toprated_movies()
    if titles:
        embed.add_field(name='**Movies:**', value='\n'.join(titles), inline=False)
    else:
        embed.add_field(name='**Movies:**', value='Error, movies not found', inline=False)
    
    await ctx.message.delete()
    await ctx.send(embed=embed)


#Evento que devuelve un saludo al escribir 'Hi'
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if 'hi' in message.content.lower():
        await message.channel.send(f'Hi {message.author.name}!')

    await bot.process_commands(message)


bot.run(token)