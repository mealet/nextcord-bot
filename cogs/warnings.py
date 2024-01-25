import nextcord
from nextcord.ext import commands
from datetime import timedelta
from datetime import datetime
import config
import sqlite3

# database init
db = sqlite3.connect('database.db')
c = db.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS `warns` (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER,
                                w_count INTEGER
)
""")
db.commit()

async def warns_update(bot):
    print("[COGS][WARNINGS] warns_update() called")
    c.execute("SELECT * FROM `warns`")
    warns_list = c.fetchall()
    if len(warns_list) > 0:
        for i in range(len(warns_list)):
            user_id = warns_list[i][1]
            user_ = await bot.fetch_user(user_id)
            if warns_list[i][2] >= 3:
                try:
                    gld = bot.get_guild(config.guild_id)
                    member_ = gld.get_member(user_id)
                    await member_.edit(timeout=nextcord.utils.utcnow() + timedelta(minutes=120))
                    c.execute(
                        f"INSERT INTO `mutes_log` (user_muted, args, reason, moderator, datetime) VALUES ({user_id}, '120 mins', '3 Warnings', 'AutoMod', '{datetime.now().strftime('%d.%m.%Y %H:%M')}')")
                    db.commit()
                    c.execute(f"UPDATE `warns` SET w_count=0 WHERE user_id={user_id}")
                    db.commit()
                    print(f"[COGS][WARNINGS] User ID:{user_id} muted by AutoMod because warnings >= 3")
                    print(f"[COGS][WARNINGS] Updated warns (w_count=0) for user ID:{user_id}")
                except PermissionError:
                    print(f"[COGS][WARNINGS] Permission error with muting {user_.name}. Removing warns...")
                    c.execute(f"UPDATE `warns` SET w_count=0 WHERE user_id={user_id}")
                    db.commit()

    else:
        pass

async def warn_user(user_id):
    print(f"[COGS][WARNINGS] warn_user({user_id}) called")
    c.execute(f"SELECT w_count FROM `warns` WHERE user_id={user_id}")
    current_warns = c.fetchall()
    if len(current_warns) > 0:
        c.execute(f"UPDATE `warns` SET w_count={current_warns[0][0] + 1} WHERE user_id={user_id}")
        db.commit()
        print(f"[COGS][WARNINGS] Updated warns (w_count={current_warns[0][0] + 1}) for user ID:{user_id}")
    else:
        c.execute(f"INSERT INTO `warns` (user_id, w_count) VALUES ({user_id}, 1)")
        db.commit()
        print(f"[COGS][WARNINGS] Updated warns (w_count=1) for user ID:{user_id}")


class Warnings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await warns_update(self.bot)



def setup(bot):
    bot.add_cog(Warnings(bot))