import os
import nextcord
from nextcord.ext import commands
import config
import dotenv

dotenv.load_dotenv("settings.env")
intents = nextcord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot started!")
    await bot.change_presence(status=nextcord.Status.online, activity=nextcord.Game(name="by mealet"))

if __name__ == "__main__":
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            bot.load_extension(f"cogs.{file[:-3]}")
    bot.run(os.environ.get("TOKEN"))