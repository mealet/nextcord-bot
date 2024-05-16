# 🌐 | Nextcord Bot
<dev id="badges">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.11-blue?style=flat"></a>
  <a href="https://nextcord.dev/"><img src="https://img.shields.io/badge/Nextcord-library-blue?style=flat"></a>
  <a href="https://docs.python.org/3/library/sqlite3.html"><img src="https://img.shields.io/badge/Sqlite3-library-blue?style=flat"></a>
  <a href="https://docs.python.org/3/library/asyncio.html"><img src="https://img.shields.io/badge/Asyncio-library-blue?style=flat"></a>
<a href=https://docker.com"><img src="https://img.shields.io/badge/Docker-engine-blue?style=flat"></a>
</dev>

## 📧 | Description
This is a testing bot created to learn nextcord library, and test some new discord features.
Bot have database, which is creating on start (`database.db`), and some cogs. You can use it for free, but bot created on russian language,
so you must replace 70-80% strokes in code. I wrote translate to english in comments for you, but for other languages you need to use translator 👀.

Project licensed under the MIT License. Check [LICENSE](./LICENSE) file for details.

To start using bot first create application on [Discord Developer Portal](https://discord.com/developers/applications), select the name, picture and description for him.
After that invite your application to your server and copy token. Where you have to past token I described in "Installation" paragraph.

## 👇 | Features
- Bot have database (`database.db`) with moderation logs
- Database creating on first bot start
- Roles by selecting option from list in special channel | [roles.py](/cogs/roles.py)
- You can add your custom roles to dropdown menu in config | [config.py](/config.py)
> To add your role write your role in `roles` object like: `"role_custom_id": [role_id, "Role Description", "Label in list", "Emoji 👀"]`
> Example:
> ```
> roles = {
>   "games": [1183105489207304202, 'Search friends and teammates for games', "Games", "🎮"]
> }
> ```
- Moderator applications created with modal windows | [applications.py](/cogs/applications.py)
- Moderation commands "Ban", "Kick", "Mute" are in user dropdown menu item "Apps" | [app.py](/cogs/app.py)
- Moderation commands have logs in database, you can check it by commands `mute_logs`, `kick_logs`, `ban_logs`
- Chat auto-moderation detecting bad words in chat and warning. Moderation roles from config will not get warns | [banWords.py](/cogs/banWords.py)
- Warning system with table in database. After 3 warnings user getting 120 mins mute. You can call `warns_update` and `warn_user` in any cog, or main module | [warnings.py](/cogs/warnings.py)
- Bot have ticket system. After deleting ticket bot sending embed message with information and moving channel to "Closed tickets" category | [tickets.py](/cogs/tickets.py)
- Ticket's transcription sending in channel and to user DM | [tickets.py](/cogs/tickets.py)
- Bot showing server statistics by creating voice channels in category from config. | [serverStats.py](/cogs/serverStats.py)
- Bot have manual logging system | [logs.py](/cogs/logs.py)
- Logs saving into the log file in `/logs/` folder | [logs.py](/cogs/logs.py)

## 💫 | Installation
Mini navigation: [Windows](README.md#Windows), [Linux](README.md#Linux), [Notes, Tips and etc.](README.md#Notes)

### Notes

> [!TIP]
> - To open console in main directory find directory path at top and click on empty place, then write `cmd` and press enter.
> - To copy channel or guild id enable developer mode in settings, press right button on channel/guild/role/user/message and etc. and choose `Copy ID`

> [!IMPORTANT]
> ### Config parameters
> - `guild_id` - your server id.
>   **_Channels:_**
> - `apps_channel_id` - id of moderator applications channel. Bot will send embed message and button for modal window.
> - `apps_get_id` - id of channel where moderator applications sending after submitting.
> - `roles_channel_id` - id of channel where bot sending message embed and dropdown menu with roles.
> - `tickets_channel_id` - channel where sending embed message with button for create ticket.
>   **_Categories:_**
> - `tickets_category` - category, where creating tickets after pressing button.
> - `closed_tickets_category` - category, where closed tickets moving.
> - `stats_category` - category, where bot creating voice channel to show statistics.
>   **_Roles:_**
> - `roles` - roles for selecting from dropdown menu.
> - `moderation_roles` - roles, which not getting warns by automod.
> - `tickets_roles` - roles, which getting access to tickets.
> - `tech_moderator_role` - members with this role can get access to logs and statsUpdate.
>   **_Params:_**
> - `bot_logger_message` - message which writing in logs file on start

### 🔵 | Windows
1. Install Python from Official Site.
2. Download bot's source code.
3. Go to main directory and run commands:
```
pip install -r requirements.txt
```
```
echo TOKEN=*YOUR BOT TOKEN* > settings.env
```

4. Open `config.py` and edit parameters for your server.
5. Run bot:
```
python main.py
```

### 🔴 | Linux
1. Install requirements:
```
sudo apt update & sudo apt upgrade
sudo apt install python3
sudo apt install python3-pip
apt install git
```
2. Clone repository:
```
git clone https://github.com/mealet/nextcord-bot.git
```
3. Install pip libraries:
```
cd nextcord-bot
pip3 install -r requirements.txt.
```
4. Set your app token in environment:
```
echo TOKEN=*YOUR BOT TOKEN* > settings.env
```
5. Edit parameters for your server in `config.py`.

6. Run main script:
```
python3 main.py
```

### 🟢 | Docker
1. Install docker and docker compose plugin.
2. Clone repository and go to it's directory.
3. Run docker:
```
systemctl start docker
```
<sup>On windows just start _Docker Desktop_</sup>

4. Build image:
```
docker-compose build
```
5. Start it in the daemon mode:
```
docker-compose up -d
```
6. Check bot logs:
```
docker-compose logs
```

## 🔗 | Links
- Python - https://www.python.org/
- Nextcord Docs - https://docs.nextcord.dev/
- Sqlite3 Docs - https://docs.python.org/3/library/sqlite3.html
- Asyncio Docs - https://docs.python.org/3/library/asyncio.html
- Docker - https://www.docker.com/
