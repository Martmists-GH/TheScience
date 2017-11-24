import math

def get_xp_needed(level):
    return level * math.log(level)


class Level:
    def __init__(self, bot):
        role = bot.config.scientist_role
        data = bot.data
