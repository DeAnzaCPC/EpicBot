from discord.ext import commands
from discord.ext import tasks
from tinydb import TinyDB, Query
import re


class Battle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.battles = {}
        self.opps = {}

    @staticmethod
    def returnAtCoderID(id_list):
        res = []
        q = Query()
        db = TinyDB('json/account.json')
        for item in id_list:
            if not re.match(r"<@(\d{18})>", item):
                return -1  # -1: not discord tag
            s = db.search(q.discordID == item[2:-1])
            if not s:
                return 0  # 0: discord id not found in database
            else:
                res.append(s[0]['atcoderID'])
        return res

    @commands.command()
    async def battle(self, ctx, handle1: str, handle2: str):

        res = self.returnAtCoderID([handle1, handle2])
        if res == -1:
            await ctx.send("Invalid input! Please follow this format: `!battle [discord-ping 1] [discord-ping 2]`")
            return
        elif res == 0:
            await ctx.send("User AtCoder ID not found in database!")
            return

        [handle1, handle2] = res
        pid = self.bot.oj.select_problem(handle1, handle2)
        self.battles[handle1] = pid
        self.battles[handle2] = pid
        self.opps[handle1] = handle2
        self.opps[handle2] = handle1
        await ctx.send(self.bot.oj.get_url(pid))

    @commands.command()
    async def confirm(self, ctx, handle: str):
        pid = self.battles[handle]
        opp = self.opps[handle]
        winner = self.decide_winner(handle, opp, pid)
        if winner is None:
            await ctx.send("No winner yet")
        else:
            await ctx.send("Winner is " + winner + "! They solved it first!")

    def decide_winner(self, handle1, handle2, pid):
        submits1 = self.bot.oj.fetch_submissions(handle1, pid)
        submits2 = self.bot.oj.fetch_submissions(handle2, pid)
        handles = [handle1, handle2]
        combined_ac = []
        for s in submits1:
            if s.is_ac:
                combined_ac.append((s.timestamp, 0))
        for s in submits2:
            if s.is_ac:
                combined_ac.append((s.timestamp, 1))
        if len(combined_ac) == 0:
            return None
        combined_ac = sorted(combined_ac)
        return handles[combined_ac[0][1]]


def setup(bot):
    bot.add_cog(Battle(bot))
