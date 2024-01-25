import nextcord
from nextcord.ext import commands
import config
from datetime import datetime

class Applications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        # Sending embed message with button on bot start
        _guild = self.bot.get_guild(config.guild_id)
        apps_channel = nextcord.utils.get(_guild.channels, id=config.apps_channel_id)

        apps_embed = nextcord.Embed(title="Заявка на модератора")
        apps_embed.add_field(name="Информация", value="Чтобы подать заявку на модератора нажмите на кнопку ниже и заполните заявку", inline=False)
        apps_embed.add_field(name="Требования", value="14 лет\nАдекватность\nСтрессоустойчивость", inline=False)
        apps_embed.set_image(url="https://media.giphy.com/media/gfm4EwaaCuonzi9gaX/giphy.gif")


        # callback for button
        async def button_callback(inter):
            # callback for modal window
            async def modal_callback(inter):
                app_embed = nextcord.Embed(colour=nextcord.Colour.blue(), timestamp=datetime.now())
                app_embed.add_field(name="Ваше имя", value=f"*{txt_input1.value}*", inline=False)
                app_embed.add_field(name="Ваша дата рождения", value=f"*{txt_input2.value}*", inline=False)
                app_embed.add_field(name="Имеется ли опыт в модерации?", value=f"*{txt_input3.value}*", inline=False)
                if inter.user.avatar is not None:
                    app_embed.set_author(
                        name=inter.user.name,
                        icon_url=inter.user.avatar.url
                    )
                else:
                    app_embed.set_author(
                        name=inter.user.name,
                        icon_url="https://cdn.icon-icons.com/icons2/2108/PNG/512/discord_icon_130958.png"
                    )

                apps_get_channel = nextcord.utils.get(inter.guild.channels, id=config.apps_get_id)
                await apps_get_channel.send(embed=app_embed)
                # sending to channel which id is in config.py
                return await inter.response.send_message("Заявка отправлена", ephemeral=True)


            # creating modal window and setting callback
            mdl = nextcord.ui.Modal(title="Заявка на модератора")
            txt_input1 = nextcord.ui.TextInput(label="Ваше имя", required=True, placeholder="Иван")
            txt_input2 = nextcord.ui.TextInput(label="Ваша дата рождения", required=True, placeholder="01.01.2001")
            txt_input3 = nextcord.ui.TextInput(label="Имеется ли опыт в модерации?", required=True, placeholder="Да/Нет")
            mdl.add_item(txt_input1)
            mdl.add_item(txt_input2)
            mdl.add_item(txt_input3)
            mdl.callback = modal_callback

            await inter.response.send_modal(mdl)


        # creating button setting callback and adding view for it
        btn = nextcord.ui.Button(style=nextcord.ButtonStyle.green, label="Подать заявку", custom_id="do_app")
        btn.callback = button_callback
        _view = nextcord.ui.View(timeout=0)
        _view.add_item(btn)

        await apps_channel.purge()
        await apps_channel.send(embed=apps_embed, view=_view)


def setup(bot):
    bot.add_cog(Applications(bot))