import nextcord
from nextcord.ext import commands
from datetime import datetime
from datetime import timedelta
import config
import sqlite3
import asyncio

database = sqlite3.connect("database.db")
cursor = database.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS kicks_log (
    kick_id     INTEGER   PRIMARY KEY AUTOINCREMENT,
    user_kicked INTEGER,
    reason      TEXT (18),
    moderator   INTEGER,
    datetime    TEXT
); """)

database.commit()

cursor.execute("""CREATE TABLE IF NOT EXISTS bans (
    ban_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    user_banned INTEGER,
    until       TEXT,
    reason      TEXT,
    moderator   TEXT,
    datetime    TEXT
);
""")

database.commit()

cursor.execute("""CREATE TABLE IF NOT EXISTS bans_log (
    ban_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    user_banned INTEGER,
    until       TEXT,
    reason      TEXT,
    moderator   TEXT,
    datetime    TEXT
);
""")

database.commit()

cursor.execute("""CREATE TABLE IF NOT EXISTS mutes_log (
    mute_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    user_muted INTEGER,
    args       TEXT,
    reason      TEXT,
    moderator   TEXT,
    datetime    TEXT
);
""")

database.commit()


class App(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        cursor.execute("SELECT * FROM `bans`;")
        guild = self.bot.get_guild(config.guild_id)
        bans_list = cursor.fetchall()
        print("Текущие баны:")
        if len(bans_list) > 0:
            for i in range(len(bans_list)):
                user_b_id = bans_list[i][1]
                current_reason = bans_list[i][3]
                current_id = bans_list[i][0]
                try:
                    user_b = await self.bot.fetch_user(user_b_id)
                    until_date = bans_list[i][2]
                    until_datetime = datetime(year=int(until_date.split(".")[2]), month=int(until_date.split(".")[1]), day=int(until_date.split(".")[0]))
                    t_left = until_datetime - datetime.now()
                    if t_left.seconds < 20:
                        try:
                            await guild.unban(user_b)
                            cursor.execute(f"DELETE FROM `bans` WHERE user_banned={user_b_id}")
                            database.commit()
                        except nextcord.errors.NotFound:
                            print(f"Бан ID:{str(current_id)} не найден")
                    else:
                        print(
                            f"{user_b.name} | {user_b_id} || Осталось секунд: {t_left.seconds} || Причина: {current_reason}")
                        await asyncio.sleep(t_left.seconds)
                        try:
                            await guild.unban(user_b)
                            cursor.execute(f"DELETE FROM `bans` WHERE user_banned={user_b_id}")
                            database.commit()
                        except nextcord.errors.NotFound:
                            print(f"Бан ID:{str(current_id)} не найден")

                except:
                    print(f"Ошибка с выводом бана (ID={current_id})")
        else:
            print("На текущий момент банов нет")

    @nextcord.slash_command(name="kick_logs")
    async def kick_logs(self, inter):
        if nextcord.utils.get(inter.guild.roles, id=1197964731261132920) in inter.user.roles:
            logs_embed = nextcord.Embed(colour=nextcord.Colour.red())
            cursor.execute("SELECT * FROM `kicks_log`;")
            k_list = cursor.fetchall()

            if len(k_list) != 0:
                for i in range(len(k_list)):
                    logs_embed.add_field(name=f"ID:{k_list[i][0]}", value=f"Kicked User: <@{k_list[i][1]}> | {k_list[i][1]}\nReason: {k_list[i][2]}\nModerator: <@{k_list[i][3]}> | {k_list[i][3]}\nDatetime: {k_list[i][4]}", inline=False)
            else:
                logs_embed.add_field(name="Empty", value="There are no kicks now")

            await inter.response.send_message(embed=logs_embed, ephemeral=True)

        else:
            await inter.response.send_message("Недостаточно прав", ephemeral=True)

    @nextcord.slash_command(name="ban_logs", guild_ids=[config.guild_id])
    async def current_bans(self, inter):
        if nextcord.utils.get(inter.guild.roles, id=1197964731261132920) in inter.user.roles:
            logs_embed = nextcord.Embed(colour=nextcord.Colour.red())
            cursor.execute("SELECT * FROM `bans_log`;")
            b_list = cursor.fetchall()

            if len(b_list) != 0:
                for i in range(len(b_list)):
                    logs_embed.add_field(name=f"ID:{b_list[i][0]}",
                                         value=f"Banned User: <@{b_list[i][1]}> | {b_list[i][1]}\nReason: {b_list[i][3]}\nModerator: <@{b_list[i][4]}> | {b_list[i][4]}\nDatetime: {b_list[i][5]}\nUntil: {b_list[i][2]}",
                                         inline=False)

            else:
                logs_embed.add_field(name="Empty", value="There are no bans now")

            await inter.response.send_message(embed=logs_embed, ephemeral=True)

        else:
            await inter.response.send_message("Недостаточно прав", ephemeral=True)

    @nextcord.slash_command(name="bans", guild_ids=[config.guild_id])
    async def bans(self, inter):
        if nextcord.utils.get(inter.guild.roles, id=1197964731261132920) in inter.user.roles:
            logs_embed = nextcord.Embed(colour=nextcord.Colour.red())
            cursor.execute("SELECT * FROM `bans`;")
            b_list = cursor.fetchall()
            if len(b_list) != 0:
                for i in range(len(b_list)):
                    logs_embed.add_field(name=f"ID:{b_list[i][0]}",
                                         value=f"Banned User: <@{b_list[i][1]}> | {b_list[i][1]}\nReason: {b_list[i][3]}\nModerator: <@{b_list[i][4]}> | {b_list[i][4]}\nDatetime: {b_list[i][5]}\nUntil: {b_list[i][2]}",
                                         inline=False)

            else:
                logs_embed.add_field(name="Empty", value="There are no bans now")

            await inter.response.send_message(embed=logs_embed, ephemeral=True)

        else:
            await inter.response.send_message("Недостаточно прав", ephemeral=True)

    @nextcord.slash_command(name="unban", guild_ids=[config.guild_id])
    async def unban(self, inter, user_id):
        if nextcord.utils.get(inter.guild.roles, id=1061676025077051502) in inter.user.roles:
            user_banned = await self.bot.fetch_user(user_id)
            guild = self.bot.get_guild(config.guild_id)
            await guild.unban(user_banned)
            cursor.execute(f"DELETE FROM `bans` WHERE user_banned={int(user_id)}")
            database.commit()
            await inter.response.send_message(f"Пользователь (<@{user_id}> | ID:{user_id}) разбанен")
        else:
            await inter.response.send_message("Недостаточно прав", ephemeral=True)



    @nextcord.user_command(name="Ban")
    async def ban(self, inter, member: nextcord.Member):
        if nextcord.utils.get(inter.guild.roles, id=1061676025077051502) in inter.user.roles:

            async def ban_modal_callback(inter):
                ban_embed = nextcord.Embed(colour=nextcord.Colour.blue(), timestamp=datetime.now())
                ban_embed.add_field(name="Бан пользователя", value=f"Пользователь: {member.mention}\nКол-во дней: {ban_days.value}\nПричина: {ban_reason.value}\nМодератор: {inter.user.mention}")
                if inter.user.avatar != None:
                    ban_embed.set_author(name=inter.user.name, icon_url=inter.user.avatar.url)
                else:
                    ban_embed.set_author(name=inter.user.name, icon_url="https://cdn.icon-icons.com/icons2/2108/PNG/512/discord_icon_130958.png")

                if member.avatar != None:
                    ban_embed.set_thumbnail(url=member.avatar.url)
                else:
                    ban_embed.set_thumbnail(url="https://cdn.icon-icons.com/icons2/2108/PNG/512/discord_icon_130958.png")

                await inter.send(embed=ban_embed)
                await member.ban(reason=ban_reason.value)
                until_date = datetime.now() + timedelta(days=int(ban_days.value))
                cursor.execute(f"INSERT INTO `bans` (user_banned, until, reason, moderator, datetime) VALUES ({member.id}, '{until_date.strftime('%d.%m.%Y')}', '{ban_reason.value}', '{inter.user.id}', '{datetime.now().strftime('%d.%m.%Y %H:%M')}')")
                database.commit()
                cursor.execute(
                    f"INSERT INTO `bans_log` (user_banned, until, reason, moderator, datetime) VALUES ({member.id}, '{until_date.strftime('%d.%m.%Y')}', '{ban_reason.value}', '{inter.user.id}', '{datetime.now().strftime('%d.%m.%Y %H:%M')}')")
                database.commit()
                await asyncio.sleep(int(ban_days.value)*60*60*24)
                try:
                    await member.unban()
                except nextcord.errors.NotFound:
                    cursor.execute(f"SELECT ban_id FROM `bans` WHERE user_banned={member.id}")
                    current_ban_id = cursor.fetchall()
                    print(f"Бан ID:{str(current_ban_id)} не найден")
                    cursor.execute(f"DELETE FROM `bans` WHERE user_banned={member.id}")
                    database.commit()

            ban_modal = nextcord.ui.Modal(title=f"Бан {member.name}")
            ban_days = nextcord.ui.TextInput(label="Введите кол-во дней бана", required=True, placeholder="7", style=nextcord.TextInputStyle.short)
            ban_reason = nextcord.ui.TextInput(label="Введите причину", required=True, placeholder="Потому", style=nextcord.TextInputStyle.short)
            ban_modal.add_item(ban_days)
            ban_modal.add_item(ban_reason)
            ban_modal.callback = ban_modal_callback

            await inter.response.send_modal(ban_modal)

        else:
            await inter.response.send_message("Недостаточно прав", ephemeral=True)

    @nextcord.user_command(name="Kick", guild_ids=[config.guild_id])
    async def kick(self, inter: nextcord.Interaction, member: nextcord.Member):

        if nextcord.utils.get(inter.guild.roles, id=1061676025077051502) in inter.user.roles:
            async def kick_modal_callback(inter):
                kick_embed = nextcord.Embed(colour=nextcord.Colour.blue(), timestamp=datetime.now())
                kick_embed.add_field(name=f"Кик пользователя",
                                     value=f"Пользователь: {member.mention}\nПричина: {kick_reason.value}\nМодератор: {inter.user.mention}")
                if inter.user.avatar != None:
                    kick_embed.set_author(name=inter.user.name, icon_url=inter.user.avatar.url)
                else:
                    kick_embed.set_author(name=inter.user.name,
                                          icon_url="https://cdn.icon-icons.com/icons2/2108/PNG/512/discord_icon_130958.png")

                if member.avatar != None:
                    kick_embed.set_thumbnail(url=member.avatar.url)
                else:
                    kick_embed.set_thumbnail(
                        url="https://cdn.icon-icons.com/icons2/2108/PNG/512/discord_icon_130958.png")
                await inter.send(embed=kick_embed)
                await member.kick(reason=kick_reason.value)
                cursor.execute(
                    f"INSERT INTO kicks_log (user_kicked, reason, moderator, datetime) VALUES ({member.id}, '{kick_reason.value}', {inter.user.id}, '{datetime.now().strftime('%d.%m.%Y %H:%M')}');")
                database.commit()

            kick_modal = nextcord.ui.Modal(title=f"Кик {member.name}")
            kick_reason = nextcord.ui.TextInput(label="Введите причину", custom_id="reason", required=True,
                                                placeholder="Потому что", max_length=18,
                                                style=nextcord.TextInputStyle.short)
            kick_modal.add_item(kick_reason)
            kick_modal.callback = kick_modal_callback
            await inter.response.send_modal(kick_modal)

        else:
            await inter.response.send_message("Недостаточно прав", ephemeral=True)

    @nextcord.user_command(name="Mute")
    async def mute(self, inter, member: nextcord.Member):
        if nextcord.utils.get(inter.guild.roles, id=1061676025077051502) in inter.user.roles:

            async def mute_modal_callback(inter):
                mute_embed = nextcord.Embed(colour=nextcord.Colour.blue())
                mute_embed.add_field(name="Мут пользователя",
                                     value=f"Пользователь: {member.mention}\nВремя: {mute_time.value} минут\nПричина: {mute_reason.value}\nМодератор: {inter.user.mention}")
                if inter.user.avatar != None:
                    mute_embed.set_author(name=inter.user.name, icon_url=inter.user.avatar.url)
                else:
                    mute_embed.set_author(name=inter.user.name,
                                          icon_url="https://cdn.icon-icons.com/icons2/2108/PNG/512/discord_icon_130958.png")

                if member.avatar != None:
                    mute_embed.set_thumbnail(url=member.avatar.url)
                else:
                    mute_embed.set_thumbnail(
                        url="https://cdn.icon-icons.com/icons2/2108/PNG/512/discord_icon_130958.png")

                await inter.send(embed=mute_embed)
                await member.edit(timeout=nextcord.utils.utcnow() + timedelta(minutes=int(mute_time.value)))
                cursor.execute(
                    f"INSERT INTO `mutes_log` (user_muted, args, reason, moderator, datetime) VALUES ({member.id}, '{mute_time.value} mins', '{mute_reason.value}', '{inter.user.id}', '{datetime.now().strftime('%d.%m.%Y %H:%M')}')")
                database.commit()


            mute_modal = nextcord.ui.Modal(title=f"Мут {member.name}")
            mute_time = nextcord.ui.TextInput(label="Введите время мута в минутах", required=True)
            mute_reason = nextcord.ui.TextInput(label="Введите причину", required=True)
            mute_modal.add_item(mute_time)
            mute_modal.add_item(mute_reason)
            mute_modal.callback = mute_modal_callback
            await inter.response.send_modal(modal=mute_modal)
        else:
            await inter.response.send_message("Недостаточно прав", ephemeral=True)

    @nextcord.slash_command(name="unmute")
    async def unmute(self, inter, member: nextcord.Member):
        if nextcord.utils.get(inter.guild.roles, id=1061676025077051502) in inter.user.roles:
            await inter.response.send_message(f"Пользователь {member.mention} размучен", ephemeral=True)
            await member.edit(timeout=None)
            cursor.execute(
                f"INSERT INTO `mutes_log` (user_muted, args, reason, moderator, datetime) VALUES ({member.id}, 'Unmute', 'Unmute', '{inter.user.id}', '{datetime.now().strftime('%d.%m.%Y %H:%M')}')")
            database.commit()
        else:
            await inter.response.send_message("Недодстаточно прав", ephemeral=True)

    @nextcord.slash_command(name="mute_logs")
    async def mute_logs(self, inter):
        if nextcord.utils.get(inter.guild.roles, id=1197964731261132920) in inter.user.roles:
            logs_embed = nextcord.Embed(colour=nextcord.Colour.red())
            cursor.execute("SELECT * FROM `mutes_log`;")
            b_list = cursor.fetchall()

            if len(b_list) != 0:
                for i in range(len(b_list)):
                    logs_embed.add_field(name=f"ID:{b_list[i][0]}",
                                         value=f"Muted User: <@{b_list[i][1]}> | {b_list[i][1]}\nArgs: {b_list[i][2]}\nReason: {b_list[i][3]}\nModerator: <@{b_list[i][4]}> | {b_list[i][4]}\nDatetime: {b_list[i][5]}", inline=False)

            else:
                logs_embed.add_field(name="Empty", value="There are no mutes now")

            await inter.response.send_message(embed=logs_embed, ephemeral=True)

        else:
            await inter.response.send_message("Недостаточно прав", ephemeral=True)

def setup(bot):
    bot.add_cog(App(bot))