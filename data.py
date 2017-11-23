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

    async def on_member_join(self, member):
        role = [role for role in member.guild.roles if role.id == self.config.interns_role][0]
        await member.add_roles(role, reason="Role on Join")

    async def on_message(self, message):
        userid = message.author.id

        if str(userid) in self.data:
            self.data[str(userid)] += 1

        else:
            self.data[str(userid)] = 1

        await self.process_commands(message)

    def load_cogs(self):
        for cog in self.config.cogs:
            self.load_extension(cog)
