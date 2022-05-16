from .ping import Ping
cogs = [Ping]

def register(bot):
  for cls in cogs:
    bot.add_cog(cls(bot))