import math

import discord
from discord.ext import commands


def get_xp_needed(level):
    return round(level * math.log(level) * 100)


def get_xp_max_curlev(xp):
    x = 0
    level = 0
    while xp > x:
        level += 1
        x = get_xp_needed(level)
    return xp, x, level-1


class Level:
    def __init__(self, bot):
        self.log = bot.log
        self.introle = bot.config.interns_role
        self.role = bot.config.scientist_role
        self.data = bot.data

    @commands.command()
    async def level(self, ctx, user: discord.Member = None):
        lookup = user or ctx.message.author
        data = self.data.get(str(lookup.id), 0)
        current, next_, level = get_xp_max_curlev(data)
        await ctx.send(f"XP: {current}/{next_}\nLevel: {level}")

    @commands.command()
    async def rank(self, ctx, user: discord.Member = None):
        lookup = user or ctx.message.author
        sort = sorted(self.data.items(), key=lambda x: -x[1])
        data = list(enumerate(sort))
        by_id = {d[0]: (d[1], rank) for rank, d in data}
        xp, rank = by_id.get(str(lookup.id), (0, "Unknown"))
        _, _, level = get_xp_max_curlev(xp)
        top = [f"{rank+1}) {ctx.guild.get_member(int(id))} - {score}"
               for (rank, (id, score)) in data[:3]]  # noqa
        await ctx.send(f"Level: {level}\nXP: {xp}\n"
                       f"Rank: {rank+1}\n" + "\n".join(top))

    async def on_message(self, message):
        data = self.data[str(message.author.id)]
        current, next_, level = get_xp_max_curlev(data)
        if (level >= 25 and
                self.role not in [r.id for r in message.author.roles]):
            await self.log(
                f"{str(message.author)} has earned the Scientists role")
            role = [r for r in message.guild.roles if r.id == self.role][0]
            introle = [r for r in message.guild.roles
                       if r.id == self.introle][0]
            await message.author.add_roles(role)
            await message.author.remove_roles(introle)


def setup(bot):
    bot.add_cog(Level(bot))
