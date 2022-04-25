import discord
import platform
from discord.ext import commands
import datetime
import random

class Admin(commands.Cog):
  def __init__(self, client):
    self.client = client
    self.colors = {
      'WHITE': '0xFFFFFF',
      'AQUA': '0x1ABC9C',
      'GREEN': '0x2ECC71',
      'BLUE': '0x3498DB',
      'PURPLE': '0x9B59B6',
      'LUMINOUS_VIVID_PINK': '0xE91E63',
      'GOLD': '0xF1C40F',
      'ORANGE': '0xE67E22',
      'RED': '0xE74C3C',
      'NAVY': '0x34495E',
      'DARK_AQUA': '0x11806A',
      'DARK_GREEN': '0x1F8B4C',
      'DARK_BLUE': '0x206694',
      'DARK_PURPLE': '0x71368A',
      'DARK_VIVID_PINK': '0xAD1457',
      'DARK_GOLD': '0xC27C0E',
      'DARK_ORANGE': '0xA8A300',
      'DARK_RED': '0x992D22',
      'DARK_NAVY': '0x2C3E50'
      }

    self.color_list = [c for c in self.colors.values()]

  @commands.Cog.listener()
  async def on_member_join(self, member):
    channel = discord.utils.get(member.guild.text_channels, name="announcements")
    if channel:
      embed = discord.Embed(descriptrion=f"Bem-vindo a nossa Guilda! Membro n: {len(member.guild.members)} entrou", color=random.choice(self.color_list))
      embed.set_thumbnail(url=member.avatar_url)
      embed.set_author(name=member.name, icon_url=member.avatar_url)
      embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
      embed.timestamp = datetime.datetime.utcnow()

      await channel.send(embed=embed)

  @commands.Cog.listener()
  async def on_member_remove(self, member):
    channel = discord.utils.get(member.guild.text_channels, name="announcements")
    if channel:
      embed = discord.Embed(descriptrion="Um adeus de todos nós...", color=random.choice(self.color_list))
      embed.set_thumbnail(url=member.avatar_url)
      embed.set_author(name=member.name, icon_url=member.avatar_url)
      embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
      embed.timestamp = datetime.datetime.utcnow()

      await channel.send(embed=embed)

  @commands.command()
  @commands.has_permissions(administrator=True)
  async def stats(self, ctx):
    python_version = platform.python_version()
    dpy_version = discord.__version__
    server_count = len(self.client.guilds)
    member_count = len(set(self.client.get_all_members()))

    embed = discord.Embed(name=f"{self.client.user.name} Stats", description="\uFEFF", colour=ctx.author.colour, timestamp=ctx.message.created_at)
    embed.add_field(name="Bot Version", value=self.client.version)
    embed.add_field(name="Python Version", value=python_version)
    embed.add_field(name="Discord.py Version", value=dpy_version)
    embed.add_field(name="Total Guilds", value=server_count)
    embed.add_field(name="Total Users", value=member_count)
    embed.add_field(name="Bot Developers", value='<@320311084827410432>')
    embed.set_footer(text=f"Carpe Noctem | {self.client.user.name}")
    embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
    await ctx.reply(embed=embed, mention_author=False)

  @commands.command(aliases=['limpar'])
  @commands.has_permissions(manage_messages=True)
  async def purge(self, ctx, amount=5):
    if amount > 300:
      await ctx.reply("Quantidade solicitada é muito alta! Máx: 300")
    else:
      await ctx.channel.purge(limit=amount + 1)

  @commands.command()
  @commands.has_permissions(administrator=True)
  async def kick(self, ctx, member: commands.MemberConverter, *, reason=None):
    await member.kick(reason=reason)
    await ctx.reply(f"Kicked{member.mention}.", mention_author=False)

  @commands.command(aliases=['banir'])
  @commands.has_permissions(administrator=True)
  async def ban(self, ctx, member: commands.MemberConverter, *, reason=None):
    await member.ban(reason=reason)
    await ctx.reply(f"Banned {member.mention}.", mention_author=False)

  @commands.command(aliases=['desbanir'])
  @commands.has_permissions(administrator=True)
  async def unban(self, ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
      user = ban_entry.user

      if (user.name, user.discriminator) == (member_name, member_discriminator):
        await ctx.guild.unban(user)
        await ctx.reply(f'Unbanned {user.mention}.', mention_author=False)

  
def setup(client):
  client.add_cog(Admin(client))