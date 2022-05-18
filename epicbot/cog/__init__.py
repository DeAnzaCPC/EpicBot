from .ping import Ping
from .battle import Battle
cogs = [Ping, Battle]

def register(app):
  for cls in cogs:
    app.bot.add_cog(cls(app))