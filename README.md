# Nextcord Bot
<dev id="badges">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.11-blue?style=flat"></a>
  <a href="https://nextcord.dev/"><img src="https://img.shields.io/badge/Nextcord-Library-blue?style=flat"></a>
</dev>

## Description
This is a testing bot created to learn nextcord library, and test some new discord features.
Bot have database, who's creating on start (`database.db`), and some cogs.

## Features
- Bot have database (`database.db`) with moderation logs
- Database creating on first bot start
- Roles by selecting option from list in special channel | [roles.py](/cogs/roles.py)
- Moderator applications created with modal windows | [applications.py](/cogs/applications.py)
- Moderation commands "Ban", "Kick", "Mute" are in user dropdown menu item "Apps" | [app.py](/cogs/app.py)
- Moderation commands have logs in database, you can check it by commands `mute_logs`, `kick_logs`, `ban_logs`

## Installation
**Notes, tips, important, warnings, cautions:**

> [!TIP]
> - To open console in main directory find directory path at top and click on empty place, then write `cmd` and press enter.
> - To copy channel or guild id enable developer mode in settings, press right button on channel/guild/role/user/message and etc. and choose `Copy ID`

>[!IMPORTANT]
> - `guild_id` - your server id.
> - `apps_channel_id` - id of moderator applications channel. Bot will send embed message and button for modal window.
> - `apps_get_id` - id of channel where moderator applications sending after submitting.
> - `roles_channel_id` - id of channel where bot sending message embed and dropdown menu with roles.
> - `roles` - roles for selecting from dropdown menu.

### Windows
First install python from official site.
Download source code, unzip it to any place and open console in main directory.
After you opened command prompt in main directory, write next commands:
```
pip install -r requirements.txt
```
```
echo TOKEN=*YOUR BOT TOKEN* > settings.env
```

Now open `config.py` in any code editor (or notepad) and edit parameters.
When you a ready to start, type:
```
python main.py
```

### Linux
Install some requirements
```
sudo apt update & sudo apt upgrade
sudo apt install python3
sudo apt install python3-pip
apt install git
```
Clone the repository
```
git clone https://github.com/mealet/nextcord-bot.git
```
Install pip requirements
```
cd nextcord-bot
pip3 install -r requirements.txt
```
Insert your token into enviroment
```
echo TOKEN=*YOUR BOT TOKEN* > settings.env
```
Now open `config.py` in any code editor (or notepad) and edit parameters.
When you a ready to start, type:
```
python3 main.py
```

## Links
- Python - https://www.python.org/
- Nextcord Docs - https://docs.nextcord.dev/
- Sqlite3 Docs - https://docs.python.org/3/library/sqlite3.html
- Asyncio Docs - https://docs.python.org/3/library/asyncio.html
