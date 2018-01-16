import asyncio
import io

import matplotlib
matplotlib.use('Agg')
from matplotlib.pyplot import plot, savefig, close, scatter  # noqa
from numpy import linspace, poly1d, polyfit  # noqa
# from scipy.interpolate import splev, splrep  # noqa
import discord  # noqa
from discord.ext import commands  # noqa

from utils.io import JSONFile  # noqa


class StatTracker:
    def __init__(self, bot):
        self.data = bot.data
        self.data.add_update_handler(self.handle_data_update)
        self._history = JSONFile("history.json", bot.loop)
        m = 0
        for val in self._history.data.values():
            t = int(max(list(val["total"].keys()) or [], key=int))
            m = t if t > m else m
        self.current_hour = int(m)
        self._task = bot.loop.create_task(self.increase_hour())

    async def increase_hour(self):
        while True:
            await asyncio.sleep(3600)
            self.current_hour += 1

    async def handle_data_update(self, var, value):
        if var not in self._history:
            self._history[var] = {"total": {}, "delta": {}, "last": value}

        usr = self._history[var]
        h = str(self.current_hour)

        if h not in usr["delta"]:
            usr["delta"][h] = value - usr["last"]
            usr["last"] = value

        usr["total"][h] = value
        usr["delta"][h] += value - usr["delta"][h] - usr["last"]
        self._history["update_trigger"] = {"total": {"0": 0}, "delta": {}, "last": 0}

    @commands.command()
    async def history(self, ctx, user: discord.Member = None):
        lookup = user or ctx.message.author
        hist = self._history.get(str(lookup.id))

        if hist is None:
            return await ctx.send("No xp changes recorded!")

        hist = hist["total"]

        s = [int(x) for x in sorted(hist, key=int)]
        start = s[0]
        end = s[-1]

        x_axis = list(range(start, end+1, 10))
        y_axis = []
        x_temp = []

        for x in x_axis:
            if x in s:
                x_temp.append(x)
                y_axis.append(hist[str(x)])

        print(x_axis, x_temp, y_axis)

        if not x_temp:
            return await ctx.send("No xp changes recorded!")

        # smoothing

        z = polyfit(x_temp, y_axis, 100)
        p = poly1d(z)

        print(z)

        s = len(z)

        x_axis = linspace(min(x_axis), max(x_axis), 5000)
        y_axis_new = p(x_axis)

        # spl = splrep(x_temp, y_axis)
        # x_axis = linspace(min(x_axis), max(x_axis), 5000)
        # y_axis_new = splev(x_axis, spl)

        # x_axis = linspace(min(x_axis), max(x_axis), 5000)
        # y_axis_new = spline(x_temp, y_axis, x_axis)

        # f = interp1d(x_temp, y_axis, kind='nearest', fill_value="extrapolate")
        # y_axis_new = f(x_axis)

        plot(x_temp, y_axis, 'o', x_axis, y_axis_new, '-')

        b = io.BytesIO()
        savefig(b, format="png")
        b.seek(0)

        close()

        await ctx.send(f"History of XP recorded for {str(lookup)} per hour",
                       file=discord.File(b, filename="History.png"))


def setup(bot):
    bot.add_cog(StatTracker(bot))
