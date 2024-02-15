import nextcord
from nextcord.ext import commands
import asyncio
import config
import colorama
from colorama import Back, Fore, Style
from datetime import datetime
import os
import other

# init
if len(os.listdir('./logs')) > 7:
    other.directory_clear("./logs")

log_file = open(f"logs/log_{datetime.now().strftime('%d.%m.%Y_%H.%M.%S')}.txt", "a")

def close_logging_file(log_file):
    log_file.close()

def write_log_file(log_file, log_message):
    log_file.write("\n"+log_message)

def _log(log_file, log_message):
    print(log_message)
    log_file.write("\n"+log_message)

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        _log(log_file, "[COGS][LOGS] Logger started")
    
    # message logger
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        # CID - Channel ID
        # AID - Author ID
        print(Back.WHITE + Fore.BLACK + Style.DIM)
        _log(log_file, f"[MESSAGE][CID:{message.channel.id}][AID:{message.author.id}]: {message.content}")
        _log(log_file, f"|----[COMPONENTS]: {len(message.components)} item(s)")
        _log(log_file, f"|----[ATTACHMENTS]: {message.attachments}")
        _log(log_file, f"|----[STICKERS]: {message.stickers}")
        print(Back.RESET + Fore.RESET + Style.RESET_ALL)

def setup(bot):
    bot.add_cog(Logs(bot))