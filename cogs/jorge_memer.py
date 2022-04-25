import requests
import io
import aiohttp
import discord
from discord.ext import commands

main_url = 'https://meme-api.herokuapp.com/gimme'

def get_meme(subreddit=''):
  url = f"{main_url}{subreddit}"
  response = requests.get(url)
  meme_url = response.json()["url"]
  return meme_url

class Memer(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command()
  async def meme(self, ctx):
    """Random Memes."""
    url = get_meme(subreddit="/meme")
    async with aiohttp.ClientSession() as session:
      async with session.get(url) as resp:
          if resp.status != 200:
              return await url.send('Could not download file...')
          data = io.BytesIO(await resp.read())
          await ctx.reply(file=discord.File(data, 'meme.png'), mention_author=False)

  @commands.command(aliases=['wholesome', 'wholememes'])
  async def memesfofos(self, ctx):
    """Cute Memes."""
    url = get_meme(subreddit='/wholesomememes')
    async with aiohttp.ClientSession() as session:
      async with session.get(url) as resp:
          if resp.status != 200:
              return await url.send('Could not download file...')
          data = io.BytesIO(await resp.read())
          await ctx.reply(file=discord.File(data, 'meme.png'), mention_author=False)

  @commands.command(aliases=['memesdank', 'dank'])
  async def dankmemes(self, ctx):
    """Dank Memes."""
    url = get_meme(subreddit='/dankmemes')
    async with aiohttp.ClientSession() as session:
      async with session.get(url) as resp:
          if resp.status != 200:
              return await url.send('Could not download file...')
          data = io.BytesIO(await resp.read())
          await ctx.reply(file=discord.File(data, 'meme.png'), mention_author=False)

  @commands.command(aliases=['artememes'])
  async def artmemes(self, ctx):
    """Art Memes."""
    url = get_meme(subreddit='/ClassicArtMemes')
    async with aiohttp.ClientSession() as session:
      async with session.get(url) as resp:
          if resp.status != 200:
              return await url.send('Could not download file...')
          data = io.BytesIO(await resp.read())
          await ctx.reply(file=discord.File(data, 'meme.png'), mention_author=False)

  @commands.command(aliases=['guia'])
  async def coolguide(self, ctx):
    """Random Guides."""
    url = get_meme(subreddit='/coolguides')
    async with aiohttp.ClientSession() as session:
      async with session.get(url) as resp:
          if resp.status != 200:
              return await ctx.reply('Could not download file...', mention_author=False)
          data = io.BytesIO(await resp.read())
          await ctx.reply(file=discord.File(data, 'meme.png'), mention_author=False)

  @commands.command(aliases=['joinha', 'trofeu'])
  async def trophy(self, ctx, member: discord.Member=None):
    """Congrats, Nobody Cares."""
    embed = discord.Embed(name=f"{self.client.user.name} Stats", description="\uFEFF", 
    colour=ctx.author.colour, timestamp=ctx.message.created_at)
    embed.add_field(name="Ganhadxr", value=member.mention)
    embed.add_field(name="Prêmio dado por", value=ctx.author.mention)
    embed.set_footer(text=f"Joinha Awards {ctx.message.created_at.year}")
    embed.set_author(name="Parabéns, você acaba de ganhar o Troféu Joinha!", icon_url=member.avatar_url)

    await ctx.reply(file=discord.File('./cogs/img/trophy.png', 'joinha.png'), embed=embed, mention_author=False)

  @commands.command(aliases=['palhaço', 'palhaça', 'palhaçx'])
  @commands.is_owner()
  async def clown(self, ctx, member: discord.Member=None):
    """Marque a pessoa palhaça do Grupo."""
    embed = discord.Embed(name=f"{self.client.user.name} Stats", description="\uFEFF", 
    colour=ctx.author.colour, timestamp=ctx.message.created_at)
    embed.add_field(name="Ganhadxr", value=member.mention)
    embed.add_field(name="Prêmio dado por", value=ctx.author.mention)
    embed.set_footer(text=f"Palhaçx Awards {ctx.message.created_at.year}")
    embed.set_author(name="Parabéns, você acaba de ganhar o Troféu Palhaçx do ano!", icon_url=member.avatar_url)

    await ctx.reply(file=discord.File('./cogs/img/clown.png', 'clown.png'), embed=embed, mention_author=False)

  @commands.command()
  async def teste(self, ctx):
    emoji = "\U0001f642"
    await ctx.message.add_reaction(emoji)


def setup(client):
  client.add_cog(Memer(client))