# Main script to run, nothing fancy

import config
import data

bot = data.Bot(config)

bot.load_cogs()

bot.run()
