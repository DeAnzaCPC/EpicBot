from discord.ext import commands
from discord.ext import tasks

class Battle(commands.Cog):
  def __init__(self, app):
    self.app = app
    self.battles = {}
    self.opps = {}

  @commands.Cog.listener()
  async def on_ready(self):
    pass

  @commands.command()
  async def battle(self, ctx, handle1: str, handle2: str):
    pid = self.app.oj.select_problem(handle1, handle2)
    self.battles[handle1] = pid
    self.battles[handle2] = pid
    self.opps[handle1] = handle2
    self.opps[handle2] = handle1
    await ctx.send(self.app.oj.get_url(pid))

  @commands.command()
  async def confirm(self, ctx, handle: str):
    pid = self.battles[handle]
    opp = self.opps[handle]
    winner = self.app.oj.get_winner(handle, opp, pid)
    if winner is None:
      await ctx.send("No winner yet")
    else:
      await ctx.send("Winner is " + winner + "! They solved it first!")