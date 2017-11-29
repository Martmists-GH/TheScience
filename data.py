import datetime
import random

from discord.ext.commands import Bot as Bot_
from utils.io import JSONFile


class Bot(Bot_):
    def __init__(self, config):
        self.token = config.token
        self.config = config
        self.data = JSONFile("userdata.json")
        super().__init__(command_prefix=config.prefix)

    def run(self):
        super().run(self.token)

    async def log(self, message):
        now = datetime.datetime.now().strftime("%d/%m %H:%M:%S")
        chan = [c for c in self.guilds[0].channels
                if c.id == self.config.logchannel_id][0]
        msg = f"[{now}] {message}\n"
        await chan.send(msg)

    async def on_member_join(self, member):
        role = [role for role in member.guild.roles
                if role.id == self.config.interns_role][0]
        await member.add_roles(role)
        await self.log(f"Gave {str(member)} the Scientist role on join")

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return

        userid = message.author.id

        points = random.choice([1, 1, 1, 1, 2, 3])

        # await self.log(f"Gave {str(message.author)} {points} points")

        if str(userid) in self.data:
            self.data[str(userid)] += points

        else:
            self.data[str(userid)] = points

        await self.process_commands(message)

    def load_cogs(self):
        for cog in self.config.cogs:
            self.load_extension(cog)
