# Discord Spellbook Bot

## Description

This Discord bot allows users to add, remove, cast spells, and view a list of spells within a Discord server. It uses a combination of discord.py, discord_slash, and SQLite for database management. The bot features slash commands for easy interaction.

## Features

- **Spell Addition**: Users can add spells with a name, description, element, and level.
- **Spell Removal**: Authorized users (with ban members permission) can remove spells from the database.
- **Spell Casting**: Users can cast spells on each other, showcasing the bot's interactive functionality.
- **Spell Listing**: Users can view a paginated list of all spells in the database, including details like the spell's name, description, element, creator, and level.

## Installation

### Prerequisites

- Python 3.6 or newer
- discord.py library
- SQLite3
- A Discord bot token

### Steps

1. Clone this repository or download the source code.
2. Install the required Python packages:

bash
```pip install discord discord-py-slash-command discord-components```

Create a database.sqlite file in the project directory and run the SQL script to create the necessary tables.
Replace DISCORD_BOT_TOKEN, GUILD_ID1, GUILD_ID2, ..., GUILD_IDn with your actual Discord bot token and server IDs in the script.
Run the bot with the command:

```python bot.py```

### Usage

- Adding a Spell: /spelladd spell_name:"Your Spell Name" spell_description:"Your Description" element:"Your Element" level:"Your Level"
- Removing a Spell: /spellremove spell_name:"Your Spell Name"
- Casting a Spell: /spellcast spell_name:"Your Spell Name" user:@User
- Viewing Spell List: /spelllist

### Contributors

Contributions are welcome! Please create an issue or submit a pull request with your proposed changes.

### License

MIT License

### Acknowledgements

Thanks to the Discord.py community for their extensive documentation and support.



