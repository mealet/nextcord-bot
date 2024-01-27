import asyncio
import nextcord
from nextcord.ext import commands
from datetime import datetime
import config


# function for update statistics
async def statsUpdate(bot):
    # getting guild and category
    guild = bot.get_guild(config.guild_id)
    statsCategory = nextcord.utils.get(guild.categories, id=config.stats_category)

    # getting members and bots count
    member_count = guild.member_count
    bot_count = len(guild.bots)

    # checking if category have no channels, or have channels less 2
    if len(statsCategory.channels) < 2 or statsCategory.channels is None:
        if len(statsCategory.channels) > 0 or statsCategory.channels is None:
            # deleting all channels in category
            for i in range(len(statsCategory.channels)):
                await statsCategory.channels[i].delete()

        # creting voice channels
        members_channel = await statsCategory.create_voice_channel(name=f"Участники: {member_count}") # "Members: "
        bots_channel = await statsCategory.create_voice_channel(name=f"Боты: {bot_count}") # "Bots: "
    else:
        # if category have channels, when we will search created channels by name
        for i in range(len(statsCategory.voice_channels)):
            if statsCategory.voice_channels[i].name.startswith("Участники:"): # "Members: "
                members_channel = nextcord.utils.get(guild.channels, id=statsCategory.voice_channels[i].id)
                await members_channel.edit(name=f"Участники: {member_count}") # "Members: "
            elif statsCategory.voice_channels[i].name.startswith("Боты:"): # "Bots: "
                bots_channel = nextcord.utils.get(guild.channels, id=statsCategory.voice_channels[i].id)
                await bots_channel.edit(name=f"Боты: {bot_count}") # "Bots: "

class ServerStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        await statsUpdate(bot=self.bot)

    @commands.Cog.listener()
    async def on_member_join(self):
        await statsUpdate(bot=self.bot)

    @commands.Cog.listener()
    async def on_member_remove(self):
        await statsUpdate(bot=self.bot)


    @nextcord.slash_command(name="stats_update", guild_ids=[config.guild_id])
    async def stats_update(self, inter):
        guild = self.bot.get_guild(config.guild_id)
        # checking if user is tech admin
        if nextcord.utils.get(guild.roles, id=config.tech_moderator_role) in inter.user.roles:
            # updating stats, sending logs to console and sending message
            await statsUpdate(bot=self.bot)
            print(f"[COGS][SERVERSTATS]: {inter.user.name} has updated server stats")
            await inter.response.send_message("Статистика сервера успешно обновлена!", ephemeral=True) # "Server stats successfuly updated!"
        else:
            await inter.response.send_message("Недостаточно прав!", ephemeral=True) # Not enough permissions!

def setup(bot):
    bot.add_cog(ServerStats(bot))