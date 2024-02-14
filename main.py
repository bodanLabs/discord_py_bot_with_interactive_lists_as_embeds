import random
import sqlite3
from discord.ext import commands
import discord
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option
from discord_components import *
import interactions
import math

TOKEN = DISCORD_BOT_TOKEN

intents = discord.Intents.all()
client = commands.Bot(command_prefix="#", intents=intents)
colors = [1752220, 1146986, 3066993, 2067276, 3447003, 2123412, 10181046, 7419530, 15277667, 11342935, 15844367,
          12745742, 15105570, 11027200, 15158332, 10038562, 9807270, 9936031, 8359053, 12370112, 3426654, 2899536,
          16776960]
db = sqlite3.connect('database.sqlite')
cursor = db.cursor()
slash = SlashCommand(client, sync_commands=True)
guild_ids = [GUILD_ID1,GUILD_ID2,...,GUILD_IDn]
color = random.choice(colors)


# on ready
@client.event
async def on_ready():
    print("Bot is ready")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Holders"))


@slash.slash(name="spelladd",
             description="Adds a spell",
             options=[create_option(
                 name="spell_name",
                 description="Enter the name of the spell",
                 option_type=interactions.OptionType.STRING,
                 required=True,
             ),
                 create_option(
                     name="spell_description",
                     description="Enter the description of the spell",
                     option_type=interactions.OptionType.STRING,
                     required=True,
                 ),
                 create_option(
                     name="element",
                     description="Enter the element of the spell",
                     option_type=interactions.OptionType.STRING,
                     required=False,
                 ),
                 create_option(
                     name="level",
                     description="Select the level of the spell",
                     option_type=interactions.OptionType.STRING,
                     required=False,
                     choices=[
                         {
                             "name": "Apprentice",
                             "value": "Apprentice"
                         },
                         {
                             "name": "Novice",
                             "value": "Novice"
                         },
                         {
                             "name": "Adept",
                             "value": "Adept"
                         },
                         {
                             "name": "Grand Master",
                             "value": "Grand Master"
                         }
                     ]
                 )], guild_ids=guild_ids)
async def spelladd(ctx: interactions.CommandContext, spell_name, spell_description, element,level):
    cursor.execute(f"SELECT spellName FROM spells")
    allSpells = cursor.fetchall()
    if spell_name.lower() in str(allSpells).lower():
        embed = discord.Embed(description="Spell already exists.")
        await ctx.send(embed=embed)
    else:
        cursor.execute(f"""INSERT INTO spells (spellName,spellDescription,spellElement,spellCreatorID,spellLevel) VALUES"""
                       f"""("{spell_name}","{spell_description}","{element}","{ctx.author.id}","{level}")""")
        db.commit()
        embed = discord.Embed(description=f"Spell added:\n"
                                          f"""Name: `{spell_name}`\n"""
                                          f"""Description: `{spell_description}`\n"""
                                          f"""Element: `{element}`\n"""
                                          f"""Level: `{level}`""", color=random.choice(colors))
        await ctx.send(embed=embed)


@slash.slash(name="spellremove",
             description="Removes a spell",
             options=[create_option(
                 name="spell_name",
                 description="Enter the name of the spell",
                 option_type=interactions.OptionType.STRING,
                 required=True,
             )], guild_ids=guild_ids)
@commands.has_permissions(ban_members=True)
async def spellremove(ctx: interactions.CommandContext, spell_name):
    cursor.execute(f"""SELECT spellName FROM spells WHERE spellName = "{spell_name}" """)
    check = cursor.fetchone()
    if check is None:
        embed = discord.Embed(description=f"""There is no spell named "{spell_name}" """, color=color)
        await ctx.send(embed=embed)
    else:
        cursor.execute(f"""DELETE FROM spells WHERE spellName = "{spell_name}" """)
        db.commit()
        embed = discord.Embed(description=f"""Spell `{spell_name}` removed by {ctx.author.name} """, color=color)
        await ctx.send(embed=embed)


@slash.slash(name="spellcast",
             description="Cast a spell",
             options=[create_option(
                 name="spell_name",
                 description="Enter the name of the spell",
                 option_type=interactions.OptionType.STRING,
                 required=True,
             ),
                 create_option(
                     name="user",
                     description="Tag person you want to cast on.",
                     option_type=interactions.OptionType.STRING,
                     required=True,
                 )], guild_ids=guild_ids)
async def spellcast(ctx: interactions.CommandContext, spell_name, user: discord.Member):
    cursor.execute(f"""SELECT spellName FROM spells WHERE spellName = "{spell_name}" """)
    check = cursor.fetchone()
    if check is None:
        embed = discord.Embed(description=f"""Spell `{spell_name}` does not exist and can't be casted.""", color=color)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(description=f"""{ctx.author.name} casted `{spell_name}` on {user}""")
        await ctx.send(embed=embed)


def predicate(message, l, r):
    def check(reaction, user):

        if reaction.message.id != message.id or user == client.user:
            return False
        if l and reaction.emoji == "⏪":
            return True
        if r and reaction.emoji == "⏩":
            return True
        return False

    return check

@slash.slash(name="spelllist",
             description="The list of spells",
             guild_ids=guild_ids)
async def spelllist(ctx: interactions.CommandContext):
    cursor.execute(f"""SELECT spellName FROM spells""")
    allSpells = cursor.fetchall()
    totalPages = int(math.ceil(len(allSpells)/9))
    embed = discord.Embed(title=f"""Full list of spells - Page 1/{totalPages}""", color=color)
    data = []
    for spell in allSpells:
        predata = []
        predata.append(spell[0])
        cursor.execute(f"""SELECT spellDescription FROM spells WHERE spellName = "{spell[0]}" """)
        description = cursor.fetchone()[0]
        predata.append(description)
        cursor.execute(f"""SELECT spellElement FROM spells WHERE spellName = "{spell[0]}" """)
        element = cursor.fetchone()[0]
        predata.append(element)
        cursor.execute(f"""SELECT spellCreatorID FROM spells WHERE spellName = "{spell[0]}" """)
        creatorID = cursor.fetchone()[0]
        cursor.execute(f"""SELECT spellLevel FROM spells WHERE spellName = "{spell[0]}" """)
        level = cursor.fetchone()[0]
        predata.append(creatorID)
        predata.append(level)
        data.append(predata)
    print(data)
    pages = int(math.ceil((len(data)/9)))
    startFrom = 0
    endTo = 9
    cur_page = 1
    for d in data[:9]:
        try:
            member = await client.fetch_user(d[3])
        except:
            member = "Unknown"
        embed.add_field(name=f"{d[0]}", value=f"""*{d[1]}*\n**Element**: `{d[2]}`\n**Level**: `{d[4]}`\nBy `{member}`""")
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("⏪")
    await msg.add_reaction("⏩")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["⏪", "⏩"]
        # This makes sure nobody except the command sender can interact with the "menu"

    while True:
        try:
            reaction, user = await client.wait_for("reaction_add", timeout=60, check=check)
            if str(reaction.emoji) == "⏩" and cur_page != pages:
                cur_page += 1
                startFrom +=9
                endTo +=9
                embed = discord.Embed(title=f""" Full list of spells - Page {cur_page}/{totalPages} """, color=color)
                for d in data[startFrom:endTo]:
                    member = await client.fetch_user(d[3])
                    embed.add_field(name=f""" {d[0]}""",
                                    value=f""" *{d[1]}*\n**Element**: `{d[2]}`\n**Level**: `{d[4]}`\nBy `{member}`""")
                await msg.edit(embed=embed)
                await msg.remove_reaction(reaction, user)

            elif str(reaction.emoji) == "⏪" and cur_page > 1:
                cur_page -= 1
                startFrom -= 9
                endTo -= 9
                embed = discord.Embed(title=f"""Full list of spells - Page {cur_page}/{totalPages}""", color=color)
                for d in data[startFrom:endTo]:
                    member = await client.fetch_user(d[3])
                    embed.add_field(name=f"{d[0]}",
                                    value=f"""*{d[1]}*\n**Element**: `{d[2]}`\n**Level**: `{d[4]}`\nBy `{member}`""")
                await msg.edit(embed=embed)
                await msg.remove_reaction(reaction, user)
            else:
                await msg.remove_reaction(reaction, user)
                # removes reactions if the user tries to go forward on the last page or
                # backwards on the first page
        except:
            break
        # ending the loop if user doesn't react after x seconds




client.run(TOKEN)
print(client.user.name)
