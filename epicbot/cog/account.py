import re
import requests
from bs4 import BeautifulSoup
from discord.ext import commands
from tinydb import TinyDB, Query

ATCODER_USER_BASE_URL = "https://atcoder.jp/users/"


class Account(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.q = Query()
        self.db = TinyDB('json/account.json')

    @commands.command()
    async def link(self, ctx, dis_u="", at_id=""):
        if not (dis_u and at_id):
            await ctx.send("Input missing!")
            return

        if not (self.checkAtCoderID(at_id) and await self.checkDiscordUser(dis_u)):
            await ctx.send("Invalid input! Please follow this format: `!link [discord-ping] [AtCoder ID]`")
            return

        r = self.updateDatabase(dis_u[2:-1], at_id)  # 0 - error, 1 - updated, 2 - added
        if r == 0:
            await ctx.send("User accounts already saved in database!")
            return
        if r == 1:
            await ctx.send("User accounts updated successfully!")
        else:
            await ctx.send("User accounts linked successfully!")
        await ctx.send(f"{dis_u} - AtCoder ID: {at_id}")

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

    def updateDatabase(self, dis_u="", at_id=""):
        s = self.db.search(self.q.discordID == dis_u)  # existing discord ID
        if s:
            if s[0]['atcoderID'] == at_id:  # only 1 max entry for each discord ID
                return 0
            self.db.update({'atcoderID': at_id}, self.q.discordID == dis_u)
            return 1

        self.db.insert({'discordID': dis_u, 'atcoderID': at_id})
        return 2


def setup(bot):
    bot.add_cog(Account(bot))
