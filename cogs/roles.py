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
        roles_description = ""
        for i in config.roles:
            roles_description = roles_description + f"\n<@&{config.roles[i][0]}> - {config.roles[i][1]}."

        roles_description = roles_description + "\n\nЧтобы удалить роль выберите её повторно."
        _guild = self.bot.get_guild(config.guild_id)
        roles_channel = nextcord.utils.get(_guild.channels, id=config.roles_channel_id)
        roles_embed = nextcord.Embed(title="Выбери роль")
        roles_embed.add_field(name="Список доступных ролей",
                              value=roles_description)
        roles_embed.set_image(url="https://media.giphy.com/media/5tiNlHkA1WdUh3jRDW/giphy.gif")

        # When bot starting this cog sending embed message with dropdown menu to special channel
        # Channel id is in config.py

        async def dropdown_callback(inter: nextcord.Interaction):
            for v in dropdown.values:
                current_role = nextcord.utils.get(inter.guild.roles, id=config.roles[v][0])
                if current_role in inter.user.roles:
                    await inter.user.remove_roles(current_role)
                else:
                    await inter.user.add_roles(current_role)

        options_list = []
        for x in config.roles:
            options_list.append(nextcord.SelectOption(label=config.roles[x][2], value=x, emoji=config.roles[x][3]))

        dropdown = nextcord.ui.Select(placeholder="Выбери роль", options=options_list, max_values=1)
        dropdown.callback = dropdown_callback

        _view = nextcord.ui.View(timeout=0)
        _view.add_item(dropdown)

        await roles_channel.purge()
        await roles_channel.send(embed=roles_embed, view=_view)

def setup(bot):
    bot.add_cog(Roles(bot))