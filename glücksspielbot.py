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
async def hallo(ctx):
    await ctx.send("Hallo ihr noobs!")
    
   

@bot.command()
async def hilfe(ctx):
    await ctx.send("Schicke Kraxy 10 🌹 um mitzumachen.\n"
        "Verwende dann den Befehl `!gamble` um teilzunehmen!\n"
        "🎲 Du hast eine 25 % Chance 50 🌹 zu gewinnen!")
    
   
    

@bot.command()   
async def gamble(ctx):
    user = str(ctx.author.id)
    now = time.time()
    zehn_tage = 10 * 24 * 60 * 60
    fuenf_tage = 5 * 24 * 60 * 60  # 5 Tage in Sekunden
    
    # Standard auf 10 Tage setzen
    cooldown_zeit = zehn_tage
    
     # Prüfen, ob der User die Rolle "Conju von Gottheit" hat
    role_name = "Conju von Gottheit"
    if any(role.name == role_name for role in ctx.author.roles):
        cooldown_zeit = 5 * 24 * 60 * 60  # 5 Tage
    
    
    last_used = cooldowns.get(user, 0)
    
    if now - last_used < cooldown_zeit:
        verbleibend = int(cooldown_zeit - (now - last_used))
        tage = verbleibend // 86400
        stunden = (verbleibend % 86400) // 3600
        minuten = (verbleibend % 3600) // 60

        await ctx.send(f"⏳ {ctx.author.mention} du kannst nur alle 10 Tage gamblen!\n Außer du hast die Rolle Conju von Gottheit, dann nur noch 5 Tage.\n Warte noch {tage} Tage, {stunden} Stunden und {minuten} Minuten.")
        return
    
    cooldowns[user] = now

    with open(cooldown_file, "w") as f:
        json.dump(cooldowns, f)



    # 25 % Gewinnchance
    if random.random() < 0.25:
        await ctx.send(f"Du hast gewonnen {ctx.author.mention}! 50 🌹 gehören dir.")
    else:
        await ctx.send("Das war wohl nix!")
        
        
@bot.command()
async def reset(ctx, member: discord.Member):
    owner_role_name = "Owner"

    # Prüfen, ob der Aufrufer die Rolle "Owner" hat
    if not any(role.name == owner_role_name for role in ctx.author.roles):
        await ctx.send("🚫 Du hast keine Berechtigung für diesen Befehl!")
        return

    user = str(member.id)
    if user in cooldowns:
        del cooldowns[user]
        with open(cooldown_file, "w") as f:
            json.dump(cooldowns, f)
        await ctx.send(f"✅ Cooldown für {member.mention} wurde zurückgesetzt.")
    else:
        await ctx.send(f"ℹ️ {member.mention} hat keinen aktiven Cooldown.")
        
 


bot.run(os.getenv("DISCORD_TOKEN"))
