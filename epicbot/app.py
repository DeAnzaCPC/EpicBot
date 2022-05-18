from discord.ext import commands
from cog import register
from oj import AtcodeOJ
from db import Database

class App:
  def __init__(self, discord_token):
    self.bot = commands.Bot(command_prefix = "!")
    self.oj = AtcodeOJ()
    self.db = Database()
    self.discord_token = discord_token
    register(self)

    extension = ['StartUp']
    for ext in extension:
        self.bot.load_extension(ext)

  def run(self):
    self.bot.run(self.discord_token)
