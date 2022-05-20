from discord.ext import commands
from discord.ext import tasks
import time
from tinydb import TinyDB, Query
import re

class Battle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.battles = {}
        self.next_battle_id = 0
        self.userid_to_battle = {}
        self.process_battle_batch.start()

    @staticmethod
    def get_user_id_from_ping(ping):
        if not re.match(r"<@(\d{18})>", ping):
            return None
        return ping[2:-1]

    @staticmethod
    def returnAtCoderID(id_list):
        res = []
        q = Query()
        db = TinyDB('json/account.json')
        for item in id_list:
            s = db.search(q.discordID == item)
            if not s:
                return 0  # 0: discord id not found in database
            else:
                res.append(s[0]['atcoderID'])
        return res

    @commands.command()
    async def battle(self, ctx, ping: str):
        user1 = str(ctx.author.id)
        user2 = Battle.get_user_id_from_ping(ping)
        if user2 is None:
            await ctx.send("Invalid input! Please follow this format: `!battle [discord-ping 1]`")
            return
        res = self.returnAtCoderID([user1, user2])
        if res == 0:
            await ctx.send("User AtCoder ID not found in database!")
            return

        [handle1, handle2] = res
        pid = self.bot.oj.select_problem(handle1, handle2)
        if user1 in self.userid_to_battle:
            self._delete_battle(self.userid_to_battle[user1])
        if user2 in self.userid_to_battle:
            self._delete_battle(self.userid_to_battle[user2])
        self._create_battle(user1, user2, pid)
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

    def _create_battle(self, user1, user2, pid):
        battle_id = self.next_battle_id
        self.next_battle_id += 1
        battle = {
            'users': [user1, user2],
            'pid': pid,
            'last_check': 0
        }
        self.userid_to_battle[user1] = battle_id
        self.userid_to_battle[user2] = battle_id
        self.battles[battle_id] = battle

    def _delete_battle(self, battle_id):
        battle = self.battles[battle_id]
        user1, user2 = battle['users']
        del self.userid_to_battle[user1]
        del self.userid_to_battle[user2]
        del self.battles[battle_id]

    @tasks.loop(seconds=2.0)
    async def process_battle_batch(self):
        for battle_id, battle in self.battles.items():
            users = battle['users']
            [handle1, handle2] = self.returnAtCoderID(users)
            pid = battle['pid']
            submits1 = self.bot.oj.fetch_submissions(handle1, pid)
            submits2 = self.bot.oj.fetch_submissions(handle2, pid)
            combined = []
            
            for s in submits1:
                combined.append((s.timestamp, 0, s.is_ac))
            for s in submits2:
                combined.append((s.timestamp, 1, s.is_ac))
            if len(combined) == 0:
                continue
            combined.sort()
            new_submissions = [s for s in combined if s[0] > battle['last_check']]
            new_ac = [s for s in new_submissions if s[2]]
            battle['last_check'] = combined[len(combined) - 1][0]
            if len(new_ac) == 0:
                # notify new submissions
                continue
            winner = users[new_ac[0][1]]
            print(winner)
            

def setup(bot):
    bot.add_cog(Battle(bot))
