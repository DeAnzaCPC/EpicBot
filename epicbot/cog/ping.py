from discord.ext import commands

class Ping(commands.Cog):
  def __init__(self, app):
    self.app = app

  @commands.Cog.listener()
  async def on_ready(self):
    pass

  @commands.command()
  async def ping(self, ctx):
    await ctx.send('Pong!')