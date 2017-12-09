import asyncio
import io

import matplotlib
matplotlib.use('Agg')
from matplotlib.pyplot import plot, savefig, close # noqa
from numpy import linspace  # noqa
from scipy.interpolate import spline  # noqa
import discord  # noqa
from discord.ext import commands  # noqa

from utils.io import JSONFile  # noqa


class StatTracker:
    def __init__(self, bot):
        self.data = bot.data
        self.data.add_update_handler(self.handle_data_update)
        self._history = JSONFile("history.json")
        self.current_hour = 0
        self._task = bot.loop.create_task(self.increase_hour())

    async def increase_hour(self):
        while True:
            await asyncio.sleep(600)
            self.current_hour += 10

    async def handle_data_update(self, var, value):
        if var not in self._history:
            self._history[var] = {}

        self._history[var][self.current_hour] = value
        self._history["update_trigger"] = 0

    @commands.command()
    async def history(self, ctx, user: discord.Member = None):
        lookup = user or ctx.message.author
        hist = self._history.get(str(lookup.id))

        if hist is None:
            return await ctx.send("No xp changes recorded!")

        s = sorted(hist)
        start = s[0]
        end = s[-1]

        x_axis = list(range(start, end+1, 15))
        y_axis = []
        x_temp = []

        for x in x_axis:
            if x in hist:
                x_temp.append(x)
                y_axis.append(hist[x])

        print(x_temp, y_axis)

        # smoothing
        x_axis_new = linspace(min(x_temp), max(x_temp), 100)
        y_axis_new = spline(x_temp, y_axis, x_axis_new)

        line, = plot(x_axis_new, y_axis_new)

        b = io.BytesIO()
        savefig(b, format="png")
        b.seek(0)

        close()

        await ctx.send(f"History of XP recorded for {str(lookup)} per min",
                       file=discord.File(b, filename="History.png"))


def setup(bot):
    bot.add_cog(StatTracker(bot))