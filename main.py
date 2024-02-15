import os
import nextcord
from nextcord.ext import commands
import config
import dotenv
import nextcord
import logging
from cogs import logs
import colorama
from colorama import Back, Fore, Style
from datetime import datetime
import other

# colorama init
colorama.just_fix_windows_console()
colorama.init()

# bot init
dotenv.load_dotenv("settings.env")
intents = nextcord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# function when bot starting
@bot.event
async def on_ready():
    logs.write_log_file(logs.log_file, config.bot_logger_message)
    logs._log(logs.log_file, "[MAIN][ON_READY] Bot Started!")
    # bot rich presence
    await bot.change_presence(status=nextcord.Status.online, activity=nextcord.Game(name="by mealet"))


# loading cogs and starting bot
if __name__ == "__main__":
    try:
        for file in os.listdir('./cogs'):
            if file.endswith('.py'):
                bot.load_extension(f"cogs.{file[:-3]}")

        bot.run(os.environ.get("TOKEN"))
    
    finally:
        other.console_clear()

        print(f"{Style.BRIGHT}Nextcord-Bot © by mealet\nhttps://github.com/mealet/nextcord-bot{Style.RESET_ALL}\n\n")
        logs.close_logging_file(logs.log_file)