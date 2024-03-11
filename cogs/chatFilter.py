from nextcord.ext import commands

from pymorphy3 import MorphAnalyzer

from cogs.warnings import warn_user, warns_update

morph = MorphAnalyzer(lang="ru") # language is Russian, but you can change it to English
triggers = ["блять", "бля", "пизда", "долбаёб", "придурок", "кретин", "ушлёпок", "говно", "еблан", "клоун", "тварь", "подонок", "чмо", "сука", "сучёнок"]
# list of bad words ( you can change it to your own list )

class chatFilter(commands.Cog):
    @commands.Cog.listener()
    async def on_message(self, message):
        for word in message.content.lower().strip().split():
            parsed_word = morph.parse(word)[0].normal_form
            if parsed_word in triggers:
                await message.delete()
                await message.channel.send(f"{message.author.mention} данное слово запрещено!\nВам было выдано предупреждение, после третьего предупреждения вы будете замучены на 2 часа!")
                await warn_user(message.author.id)
                await warns_update(self.bot)


def setup(bot):
    bot.add_cog(chatFilter(bot))