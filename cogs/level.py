import math

import discord
from discord.ext import commands


def get_xp_needed(level):
    return level * math.log(level)


class Level:
    def __init__(self, bot):
        role = bot.config.scientist_role
        data = bot.data

    @commands.command()
    async def level(self, ctx, user: discord.Member = None):
        pass


def setup(bot):
    pass
