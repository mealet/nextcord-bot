from datetime import datetime
from colorama import Fore, Back, Style

# your server id
guild_id = 1061673189765283921

# channels
apps_channel_id = 1063462165002067998
apps_get_id = 1183144659820740618
roles_channel_id = 1183101160203239434
tickets_channel_id = 1200492906184704030

# categories
tickets_category = 1200497664459014266
closed_tickets_category = 1200504042288324639
stats_category = 1200771859159982080

# roles for dropdown menu
roles = {
    "games": [1183105489207304202, 'Ищут друзей по играм и игровым тематикам', "Игры", "😎"],
    "events": [1183105429027434527, 'Участвуют в серверных мероприятиях', "Мероприятия", "🍺"],
    "news": [1183105327353311302, 'Первыми получают уведомления о новостях', "Новости", "👀"],
    "chat": [1199997669859401771, 'Получает уведомления в чате, а также имеет x2 опыта', "Чат", "🥸"],
}

# other roles
moderator_roles = [1061676025077051502, 1197964731261132920]
tickets_roles = [1200499542647386142, 1197964731261132920]
tech_moderator_role = 1197964731261132920

# params
bot_logger_message = f"{datetime.now().strftime('%d.%m.%Y %H:%M:%S')} nextcord-bot © by mealet\nhttps://github.com/mealet/nextcord-bot\n"