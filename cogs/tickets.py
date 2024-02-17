import asyncio
import nextcord
from nextcord.ext import commands
from datetime import datetime
import config
from cogs import logs
import colorama
from colorama import Back, Fore, Style
import os

# Note for me :)
# datetime.now().strftime('%d.%m.%Y %H:%M')

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        # getting guild and channel
        guild = self.bot.get_guild(config.guild_id)
        tickets_channel = nextcord.utils.get(guild.channels, id=config.tickets_channel_id)
        tickets_category = nextcord.utils.get(guild.categories, id=config.tickets_category)

        # creating embed
        tickets_embed = nextcord.Embed(colour=nextcord.Colour.red())
        tickets_embed.add_field(name="Нужна помощь? 👀", value="Нажмите на кнопку ниже, чтобы начать чат с администрацией 👇") # "Need help?", "Press on button to start chat with moderators"
        tickets_embed.set_image(url="https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExdHA0eWJuNTJhY214Mmo5NnF1YndxeTFjZ3phbWRqZnR0c200MnEydiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/hSXiJbWunRqZMr0KTE/giphy.gif")

        # button callback function
        async def ticket_button_callback(inter):
            ticket_channel = await tickets_category.create_text_channel(f"{inter.user.name}-{datetime.now().strftime('%d_%m_%Y %H_%M_%S')}")
            await ticket_channel.set_permissions(inter.user, send_messages=True, read_messages=True)
            
            # CID - Channel ID
            # AID - Author ID

            print(Back.GREEN+Fore.WHITE)
            logs._log(logs.log_file, f"[COGS][TICKETS][CID:{inter.channel.id}][AID:{inter.user.id}] {inter.user.name} created ticket.")
            print(Back.RESET+Fore.RESET)

            roles_mention_str = ""
            roles_mention_str = roles_mention_str + f"{inter.user.mention} "
            for i in range(len(config.moderator_roles)):
                current_role = nextcord.utils.get(guild.roles, id=config.tickets_roles[i])
                roles_mention_str = roles_mention_str + f"{current_role.mention} "
                await ticket_channel.set_permissions(current_role, send_messages=True, read_messages=True)

            # ticket embed
            ticket_embed = nextcord.Embed(colour=nextcord.Colour.red())
            ticket_embed.add_field(name=f"Тикет \"{ticket_channel.name}\"", value="Ваш тикет успешно создан, пожалуйста ожидайте пока модерация ответит вам.\nЗадавайте ваш вопрос чётко с указанием конкретной информацией (если таковая имеется).\nЕсли модератор ответил на ваш вопрос, или вы просто хотите закрыть тикет, нажмите на кнопку под сообщением")
            # "Your ticket successfuly created, please wait moderation answer.\nAsk your question clearly with specific info (if you have it).\nIf moderator dont asking you, or you just wanna close ticket - press on a button under the message."

            ticket_embed.set_image(url="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbzFsdXBycGp1MHJ1cmN0dzdwcnk2ZDV5aDRsYmRwd3h1Yjh0eWw5OCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l0HlNaQ6gWfllcjDO/giphy.gif")

            # remove button callback
            async def ticket_remove_callback(inter):
                await ticket_channel.set_permissions(inter.user, send_messages=False)
                print(Back.GREEN+Fore.WHITE)
                print()
                logs._log(logs.log_file, f"[COGS][TICKETS][CID:{inter.channel.id}][AID:{inter.user.id}] {inter.user.name} closed ticket.")
                print()
                print(Back.RESET+Fore.RESET)
                close_embed = nextcord.Embed(colour=nextcord.Colour.red(), timestamp=datetime.now())
                close_embed.add_field(name=f"{inter.user.name} закрыл тикет", value=f"Закрыл пользователь: {inter.user.mention}\nНазвание канала: {ticket_channel.name}\nСоздатель тикета: {roles_mention_str.split(' ')[0]}")
                # name=f"{inter.user.name} closed ticket", value=f"User closed: {inter.user.mention}\nChannel name: {ticket_channel.name}\nTicket author: {roles_mention_str.split(' ')[0]}"
                


                # saving history in html file

                ts_file = open(f"temp/{ticket_channel.name}.html", "a")

                ts_file.write(f'<h1 style="font-family: Calibri">Ticket "{ticket_channel.name}"</h1>\n')

                async for message in ticket_channel.history(oldest_first=True):
                    ts_file.write(f'<nav style="font-family: Calibri"><b>{message.author}:</b> {message.content}</nav>\n')
                
                ts_file.close()


                # sending embed with transcription file

                await ticket_channel.send(embed=close_embed, file=nextcord.File(f"temp/{ticket_channel.name}.html", force_close=True, filename="ticket.html"))
                await inter.response.send_message("Вы успешно закрыли тикет!", ephemeral=True) # You successfuly closed ticket!

                # sending transcription file to ticket's author

                ticket_author = nextcord.utils.get(guild.members, id=int(roles_mention_str.split(' ')[0].replace("<", "").replace("@", "").replace(">", "")))
                to_author_embed = nextcord.Embed()
                to_author_embed.add_field(name="Транскрипция тикета", value="Спасибо что воспользовались нашими тикетами! К сообщению прикреплён файл с транскрипцией.")
                to_author_embed.add_field(name="Зачем мне файл транскрипции?", value="Вы можете использовать его для подачи жалобы")

                await ticket_author.send(embed=to_author_embed, file=nextcord.File(f"temp/{ticket_channel.name}.html", force_close=True, filename="ticket.html"))

                os.remove(f"temp/{ticket_channel.name}.html")

                await asyncio.sleep(0.5)

                # closing ticket

                closed_tickets_category = nextcord.utils.get(guild.categories, id=config.closed_tickets_category)

                await ticket_channel.set_permissions(ticket_author, read_messages=False, send_messages=False)
                await ticket_channel.set_permissions(inter.user, read_messages=False)
                await ticket_channel.edit(category=closed_tickets_category)
                for i in range(len(config.moderator_roles)):
                    c_role = nextcord.utils.get(guild.roles, id=config.tickets_roles[i])
                    await ticket_channel.set_permissions(c_role, send_messages=False, read_messages=False)

            # remove button
            ticket_remove_button = nextcord.ui.Button(label="Закрыть тикет", style=nextcord.ButtonStyle.red, emoji="🗑️") # "Close ticket"
            ticket_remove_button.callback = ticket_remove_callback
            ticket_remove_view = nextcord.ui.View(timeout=0)
            ticket_remove_view.add_item(ticket_remove_button)

            await ticket_channel.send(roles_mention_str, embed=ticket_embed, view=ticket_remove_view)

        # creating button and view
        ticket_button = nextcord.ui.Button(label="Создать тикет", style=nextcord.ButtonStyle.primary, emoji="📧") # "Create ticket"
        ticket_button.callback = ticket_button_callback
        view_ = nextcord.ui.View(timeout=0)
        view_.add_item(ticket_button)

        # sending embed to special channel
        await tickets_channel.purge()
        await tickets_channel.send(embed=tickets_embed, view=view_)

def setup(bot):
    bot.add_cog(Tickets(bot))