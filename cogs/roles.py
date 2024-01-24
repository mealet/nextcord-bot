import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import config

# Cog
class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        _guild = self.bot.get_guild(config.guild_id)
        roles_channel = nextcord.utils.get(_guild.channels, id=config.roles_channel_id)
        roles_embed = nextcord.Embed(title="Выбери роль")
        roles_embed.add_field(name="Список доступных ролей",
                              value="<@&1183105327353311302> - Первыми получают уведомления о новостях.\n<@&1183105429027434527> - Участвуют в серверных мероприятиях\n<@&1183105489207304202> - Ищут друзей по играм и игровым тематикам.\n\nЧтобы удалить роль выберите её повторно")
        roles_embed.set_image(url="https://media.giphy.com/media/5tiNlHkA1WdUh3jRDW/giphy.gif")

        async def dropdown_callback(inter: nextcord.Interaction):
            for v in dropdown.values:
                current_role = nextcord.utils.get(inter.guild.roles, id=config.roles[v])
                if current_role in inter.user.roles:
                    await inter.user.remove_roles(current_role)
                else:
                    await inter.user.add_roles(current_role)

        role1 = nextcord.SelectOption(label="Игры", value="games", emoji="😎")
        role2 = nextcord.SelectOption(label="Мероприятия", value="events", emoji="🍺")
        role3 = nextcord.SelectOption(label="Новости", value="news", emoji="👀")
        dropdown = nextcord.ui.Select(placeholder="Выбери роль", options=[role1, role2, role3], max_values=1)
        dropdown.callback = dropdown_callback

        _view = nextcord.ui.View(timeout=0)
        _view.add_item(dropdown)

        await roles_channel.purge()
        await roles_channel.send(embed=roles_embed, view=_view)

def setup(bot):
    bot.add_cog(Roles(bot))