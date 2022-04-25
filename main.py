import os
import discord
import cogs._json as cj
from keep_alive import keep_alive
from discord.ext import commands
from cogs.jorge_musician_settings.config import config
from cogs.jorge_musician_settings.musicbot.audiocontroller import AudioController
from cogs.jorge_musician_settings.musicbot.settings import Settings
from cogs.jorge_musician_settings.musicbot import utils
from cogs.jorge_musician_settings.musicbot.utils import guild_to_audiocontroller, guild_to_settings
from cogs.jorge_musician_settings.musicbot.commands.general import General



cwd = cj.get_path()
print(f"{cwd}\n-----")

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),
                   description='Jorge', owner_is=320311084827410432, pm_help=True)

bot.version = '2.0'
music_extensions = ['musicbot.commands.music', 'musicbot.commands.general', 'musicbot.plugins.button']
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name=f"Hi, i'm {bot.user.name}. Use ! to interact wih me."))

@bot.command()
@commands.is_owner()
async def logout(ctx):
  await ctx.reply(f"Hey {ctx.author.mention}, i am now logging out. :wave:", mention_author=False)
  await bot.logout
  
@logout.error
async def logout_error(ctx, error):
  if isinstance(error, commands.ChackFailuer):
    await ctx.reply("Hey! You lack permission to use this command as you do not own the Bot", mention_author=False)
  else:
    raise error

@bot.event
async def on_command_error(ctx, error):
  ignored = (commands.CommandNotFound, commands.UserInputError)
  if isinstance(error, ignored):
    return
  
  if isinstance(error, commands.CommandOnCooldown):
    m, s = divmod(error.retry_after, 60)
    h, m = divmod(m, 60)
    if int(h) == 0 and int(m) == 0:
      await ctx.send(f"You must wait {int(s)} seconds to use this command!")
    elif int(h) == 0 and int(m) != 0:
      await ctx.send(f"You must wait {int(m)} minutes and {int(s)} seconds to use this command!")
    else:
      await ctx.send(f"You must wait {int(h)} hours, {int(m)} minutes and {int(s)} seconds to use this command!")
  elif isinstance(error, commands.CheckFailure):
    await ctx.send("Hey! You lack the permission to use this command.")
  else:
    raise error

@bot.command()
@commands.is_owner()
async def load(ctx, extension):
  bot.load_extension(f'cogs.{extension}')
  await ctx.reply(f"{extension} has been loaded.", mention_author=False)

@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
  bot.unload_extension(f'cogs.{extension}')
  await ctx.reply(f"{extension} has been unloaded.", mention_author=False)

@bot.command()
@commands.is_owner()
async def show_extensions(ctx):
  possible_extensions = []
  for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
      possible_extensions.append(f'{filename[:-3]}') 
  await ctx.reply(possible_extensions, mention_author=False)

@bot.event
async def on_guild_join(guild):
  print(guild.name)
  await register(guild)

async def register(guild):

  guild_to_settings[guild] = Settings(guild)
  guild_to_audiocontroller[guild] = AudioController(bot, guild)

  vc_channels = guild.voice_channels
  await guild.me.edit(nick=guild_to_settings[guild].get('default_nickname'))
  start_vc = guild_to_settings[guild].get('start_voice_channel')
  if start_vc != None:
    for vc in vc_channels:
      if vc.id == start_vc:
        await guild_to_audiocontroller[guild].register_voice_channel(vc_channels[vc_channels.index(vc)])
        await General.udisconnect(self=None, ctx=None, guild=guild)
        try:
          await guild_to_audiocontroller[guild].register_voice_channel(vc_channels[vc_channels.index(vc)])
        except Exception as e:
          print(e)
  else:
    await guild_to_audiocontroller[guild].register_voice_channel(guild.voice_channels[0])
    await General.udisconnect(self=None, ctx=None, guild=guild)
    try:
      await guild_to_audiocontroller[guild].register_voice_channel(guild.voice_channels[0])
    except Exception as e:
      print(e)

@bot.command()
@commands.is_owner()
async def r_guild(ctx):
  print(f"Registered new Guild: {ctx.guild}.")
  await register(ctx.guild)


for filename in os.listdir('./cogs'):
  if filename.endswith('.py') and not filename.startswith('_'):
    bot.load_extension(f'cogs.{filename[:-3]}')
for extension in music_extensions:
  try:
    bot.load_extension(f'cogs.jorge_musician_settings.{extension}')
  except Exception as e:
    print(e)

config.ABSOLUTE_PATH = os.path.dirname(os.path.abspath(__file__))
config.COOKIE_PATH = f"{config.ABSOLUTE_PATH}{config.COOKIE_PATH}"

keep_alive()
bot.run(os.environ['BOT_TOKEN'], bot=True)