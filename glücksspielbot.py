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

welcome_channel_id = None

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
    if welcome_channel_id is not None:
        channel = bot.get_channel(welcome_channel_id)
        if channel:
            await channel.send(f"🚀 {member.mention} ist gelandet!")
            
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
        


bot.run(os.getenv("DISCORD_TOKEN"))
