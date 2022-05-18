from discord.ext import commands
import discord


class BotStartUp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        await self.bot.change_presence(activity=discord.Game('Awaiting fiery battles...'))
        print('--------------------------')
        print(f'Logged in as: {self.bot.user.name}')
        print(f'With ID: {self.bot.user.id}')
        print('--------------------------')


def setup(bot):
    bot.add_cog(BotStartUp(bot))
