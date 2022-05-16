from discord.ext import commands
import os
from cog import register

bot = commands.Bot(command_prefix = "!")
register(bot)
bot.run(os.getenv("BOT_TOKEN"))
