import discord
from discord.ext import commands
import random
from discord.ext.commands import CommandOnCooldown
import time
import os
import json
from dotenv import load_dotenv

load_dotenv()

cooldown_file = "cooldowns.json"
ticket_file = "tickets.json"

welcome_channel_id = 1378103577825771672

# Sicheres Laden
if os.path.exists(cooldown_file):
    try:
        with open(cooldown_file, "r") as f:
            cooldowns = json.load(f)
    except json.JSONDecodeError:
        print("⚠️ Achtung: 'cooldowns.json' war beschädigt – wurde zurückgesetzt.")
        cooldowns = {}
else:
    cooldowns = {}
    
# Tickets laden
if os.path.exists(ticket_file):
    try:
        with open(ticket_file, "r") as f:
            tickets = json.load(f)
    except json.JSONDecodeError:
        print("⚠️ Achtung: 'tickets.json' war beschädigt – wurde zurückgesetzt.")
        tickets = {}
else:
    tickets = {}

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Wichtig für on_member_join

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.command()
@commands.has_permissions(administrator=True)
async def set_welcome_channel(ctx):
    global welcome_channel_id
    welcome_channel_id = ctx.channel.id
    settings["welcome_channel_id"] = welcome_channel_id
    with open(settings_file, "w") as f:
        json.dump(settings, f)
        await channel.send(f"✅ Dieser Channel ({ctx.channel.name}) ist jetzt der Willkommens-Channel!")
    

        
@bot.event
async def on_member_join(member):
    # Rolle vergeben
    role = discord.utils.get(member.guild.roles, name="Conjuror")
    if role:
        await member.add_roles(role)

    # Willkommensnachricht senden
    if welcome_channel_id is not None:
        channel = bot.get_channel(welcome_channel_id)
        if channel:
            await channel.send(f"🚀 {member.mention} ist gelandet!")
            print(f"{member} ist beigetreten!")
            
            
@bot.event
async def on_member_remove(member):
    if welcome_channel_id is not None:
        channel = bot.get_channel(welcome_channel_id)
        if channel:
            await channel.send(f"{member.mention} hat uns verlassen! Was eine Schande!")



@bot.command()
@commands.has_permissions(manage_roles=True)
async def checkroles(ctx):
    role = discord.utils.get(ctx.guild.roles, name="Conjuror")
    if not role:
        await ctx.send("❌ Die Rolle 'Conjuror' existiert nicht.")
        return

    count = 0
    for member in ctx.guild.members:
        if role not in member.roles and not member.bot:
            await member.add_roles(role)
            count += 1

    await ctx.send(f"✅ Rolle 'Conjuror' wurde {count} Mitglied(ern) gegeben.")




@bot.event
async def on_ready():
    activity = discord.Game(name="Glücksspiel 🎰")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print(f"✅ Bot ist eingeloggt als {bot.user}")


@bot.command()
async def thomasistsueß(ctx):
    await ctx.send("Kraxy sagt das stimmt!")
    
@bot.command()
async def hallo(ctx):
    await ctx.send("Hallo ihr noobs!")
    
@bot.command()
async def hilfe(ctx):
    await ctx.send(
        "Du brauchst du ein Ticket von Kraxy.\n"
        "Verwende dann den Befehl `!gamble` um teilzunehmen!\n"
        "🎲 Der Hauptpreis ist 100 🌹!\n"
        "`!anzahl` um deine Anzahl von Tickets zu einzusehen!"
    )

@bot.command()
async def commands(ctx):
    await ctx.send(
        "Liste der Commands:\n"
        "`!anzahl`: Zeigt die Anzahl deiner Tickets an.\n"
        "`!gamble`: Erlaubt dir zu gamblen und einen Preis zu gewinnen.\n"
        "`!hilfe`: Erklärt kurz wie man am Glücksspiel teilnimmt.\n"
        "`!reset @user`: Nur für Kraxy, erlaubt die Tickets eines Users auf 0 zu setzen.\n"
        "`!ticket @user anzahl`: Nur für Kraxy, gibt eine beliebige Anzahl von Tickets an einen User. Die Anzahl wird ohne Klammern oder Anführungszeichen hinter @user gesetzt.\n"
        "`!set_welcome_channel`: Setzt den Wilkommens-Channel.")
    
@bot.command()
async def abed(ctx):
    await  ctx.send("Abed ist ein sehr professioneller Conju-Spieler der leider das Wolf Game nicht gewonnen hat")
    
@bot.command()
async def kraxy(ctx):
    await ctx.send("Unser toller Vorsitzender!\nAußerdem der Host des Wolf Games und Clankriegs und der Sektenführer der Krawallmachersekte.\nNiemand ist so schlau wie er! ❤️")

@bot.command()
async def krawallmachersekte(ctx):
    await ctx.send("Die beste und gefährlichste Sekte der Welt!")
    
@bot.command()
async def git(ctx):
    await ctx.send(
        "git add .\n"
        "git commit -m \"update\"\n"
        "git push origin main\n")
    
    
    
    
    
    
    
@bot.command()
async def ticket(ctx, member: discord.Member, menge: int):
    # Rolle prüfen
    if not any(role.name == "Owner" for role in ctx.author.roles):
        await ctx.send("🚫 Du hast keine Berechtigung, Tickets zu vergeben!\nVersuchs erst gar nicht!")
        return

    user_id = str(member.id)
    tickets[user_id] = tickets.get(user_id, 0) + menge

    # Datei speichern
    with open(ticket_file, "w") as f:
        json.dump(tickets, f)

    await ctx.send(f"🎟️ {member.mention} hat jetzt {tickets[user_id]} Ticket(s)!")
    
@bot.command()
async def gamble(ctx):
    user_id = str(ctx.author.id)

    # Ticket vorhanden?
    if tickets.get(user_id, 0) <= 0:
        await ctx.send(f"{ctx.author.mention} ❌ Du brauchst ein 🎟️ Ticket von Kraxy um zu gamblen!")
        return

    # 1 Ticket abziehen
    tickets[user_id] -= 1
    with open(ticket_file, "w") as f:
        json.dump(tickets, f)

    # Ergebnisliste – 10 % je Option
    ergebnisse = [
        "DAS WAR NIX!",
        "DAS WAR NIX!",
        "DAS WAR NIX!",
        "DAS WAR NIX!",
        "DAS WAR NIX!",
        "DAS WAR NIX!",
        "DAS WAR NIX!",
        "DAS WAR NIX!",
        "DAS WAR NIX!",
        "DAS WAR NIX!",
        "DAS WAR NIX!",
        "DAS WAR NIX!",
        "DAS WAR NIX!",
        "DAS WAR NIX!",
        "DAS WAR NIX!",
        "🎉 Du gewinnst 20 🌹!",
        "🎉 Du gewinnst 40 🌹!",
        "🎉 Du gewinnst 60 🌹!",
        "🎉 Du gewinnst 80 🌹!",
        "🎉 Du gewinnst 100 🌹!",
    ]

    ergebnis = random.choice(ergebnisse)
    await ctx.send(f"{ctx.author.mention} {ergebnis}")

@bot.command()
async def reset (ctx, member: discord.Member):
    # rolle prüfen
    if not any(role.name == "Owner" for role in ctx.author.roles):
        await ctx.send("🚫 Du Frechdachs hast keine Berechtigung Tickets zurückzusetzen!")
        return
    
    user_id = str(member.id)

    if user_id in tickets and tickets[user_id] > 0:
        tickets[user_id] = 0
        with open(ticket_file, "w") as f:
            json.dump(tickets, f)
        await ctx.send(f"🧼 Die Tickets von {member.mention} wurden auf 0 gesetzt.")
    else:
        await ctx.send(f"ℹ️ {member.mention} besitzt keine Tickets.")

@bot.command()
async def anzahl(ctx):
    user_id = str(ctx.author.id)
    anzahl_tickets = tickets.get(user_id, 0)  # Hier auf das Dictionary zugreifen!
    await ctx.send(f"🎟️ {ctx.author.mention} du hast {anzahl_tickets} Tickets.")
    
    
    

# farbrollen

MESSAGE_ID = 1387916912071151767

reaction_roles = {
    "❤️": 1387907628151214193,  # Rot
    "💛": 1387907877976543354,  # Gelb
    "💚": 1387907919776976906,  # Grün
    "💙": 1387907853292933201,  # Blau
    "💜": 1387909339418853406,  # Lila
    "🩷": 1387907391940591626,  # Pink
}
        
@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id != MESSAGE_ID:
        return

    guild = bot.get_guild(payload.guild_id)
    if guild is None:
        return

    member = guild.get_member(payload.user_id)
    if member is None or member.bot:
        return

    emoji = str(payload.emoji.name)
    role_id = reaction_roles.get(emoji)
    if role_id is None:
        return

    # Alle möglichen FarbroIen (zur Sicherheit)
    color_roles = [guild.get_role(rid) for rid in reaction_roles.values()]
    user_roles = member.roles

    # Vorherige Farben entfernen
    roles_to_remove = [r for r in user_roles if r in color_roles and r.id != role_id]
    if roles_to_remove:
        await member.remove_roles(*roles_to_remove, reason="Andere Farbrollen entfernt")

    # Neue Rolle hinzufügen
    new_role = guild.get_role(role_id)
    if new_role and new_role not in user_roles:
        await member.add_roles(new_role, reason="Neue Farbe vergeben")
        print(f"{member.name} erhielt die Rolle {new_role.name}")

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id != MESSAGE_ID:
        return

    guild = bot.get_guild(payload.guild_id)
    if guild is None:
        return

    member = await guild.fetch_member(payload.user_id)
    if member is None or member.bot:
        return

    emoji = str(payload.emoji.name)
    role_id = reaction_roles.get(emoji)
    if role_id is None:
        return

    role = guild.get_role(role_id)
    if role and role in member.roles:
        await member.remove_roles(role, reason="Farbe entfernt")
        print(f"{member.name} verlor die Rolle {role.name}")
        
bot.run(os.getenv("DISCORD_TOKEN"))
