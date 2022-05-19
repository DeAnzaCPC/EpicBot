from dotenv import load_dotenv
import os
from discord.ext import commands
from oj import AtcodeOJ
from db import Database


def run(discord_token):
    bot = commands.Bot(command_prefix="!")
    bot.oj = AtcodeOJ()
    bot.db = Database()

    extension = ['battle', 'ping', 'start_up', 'account']
    for ext in extension:
        print(f'{ext} is loaded')
        bot.load_extension('cog.' + ext)
    bot.run(discord_token)


load_dotenv()
run(os.getenv("BOT_TOKEN"))
