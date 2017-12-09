import re


class Mod:
    def __init__(self, bot):
        self.log = bot.log
        self.bot = bot
        self.role = bot.config.admin_role
        self.bad_words = bot.config.bad_words

    async def on_message_update(self, before, after):
        self.on_message(after)

    async def on_message(self, message):
        if message.author.id == self.bot.user.id:
            return

        if self.role in [r.id for r in message.author.roles]:
            return

        if re.search("https?://", message.content.lower().replace(" ", "")):
            await message.delete()
            await self.log(f"Deleted a message by {str(message.author)}"
                           f" in #{message.channel.name} for having a link."
                           f"\nOriginal message: ```\n{message.content}```")

        elif any(word in message.content.lower().replace(" ", "")
                 for word in self.bad_words):
            await message.delete()
            await self.log(f"Deleted a message by {str(message.author)}"
                           f" in #{message.channel.name} for saying a bad word"
                           f".\nOriginal message: ```\n{message.content}```")


def setup(bot):
    bot.add_cog(Mod(bot))
