from discord.ext import commands
import requests
import re
from bs4 import BeautifulSoup

ATCODER_USER_BASE_URL = "https://atcoder.jp/users/"


class Account(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def link(self, ctx, dis_u="", at_id=""):
        if not (dis_u and at_id):
            await ctx.send("Input missing!")
            return

        if not (self.checkAtCoderID(at_id) and await self.checkDiscordUser(dis_u)):
            await ctx.send("Invalid input! Please follow this format: `!link [discord-ping] [AtCoder ID]`")
            return

        # TODO: Add commands to link accounts and save to database
        await ctx.send("User accounts linked successfully!")

    @staticmethod
    def checkAtCoderID(at_id):
        url = ATCODER_USER_BASE_URL + at_id
        html = requests.get(url).content
        soup = BeautifulSoup(html, 'html.parser')
        res = soup.find("div", {"data-a2a-title": "404 Not Found - AtCoder"})
        if res:
            return False
        return True

    async def checkDiscordUser(self, dis_u):
        if not re.match(r"<@(\d{18})>", dis_u):
            return False
        user = await self.bot.fetch_user(int(dis_u[2:-1]))
        if not user:
            return False
        return True


def setup(bot):
    bot.add_cog(Account(bot))
