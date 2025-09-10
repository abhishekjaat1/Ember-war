import discord
from discord.ext import commands, tasks
from mcstatus import MinecraftServer

# --- CONFIG ---
DISCORD_TOKEN = "YOUR_DISCORD_BOT_TOKEN"
PREFIX = "!"
MINECRAFT_IP = "play.yourserver.com"  # Replace with your server IP
MINECRAFT_PORT = 25565  # Replace if using custom port

# --- SETUP BOT ---
intents = discord.Intents.default()
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# --- EVENTS ---
@bot.event
async def on_ready():
    print(f"✅ {bot.user} is online!")
    update_status.start()  # start the loop when bot is ready

# --- TASK: Update Bot Status ---
@tasks.loop(seconds=60)  # update every 60 seconds
async def update_status():
    try:
        server = MinecraftServer.lookup(f"{MINECRAFT_IP}:{MINECRAFT_PORT}")
        status = server.status()
        activity = discord.Game(name=f"Ember Network – {status.players.online}/{status.players.max} online")
    except Exception:
        activity = discord.Game(name="Ember Network – Offline ❌")
    
    await bot.change_presence(activity=activity)

# --- COMMANDS ---
@bot.command()
async def status(ctx):
    try:
        server = MinecraftServer.lookup(f"{MINECRAFT_IP}:{MINECRAFT_PORT}")
        
        # Get server status
        status = server.status()
        
        # Get player list (needs enable-query=true in server.properties)
        try:
            query = server.query()
            player_names = ", ".join(query.players.names) if query.players.online > 0 else "No players online"
        except Exception:
            player_names = "⚠️ Player list unavailable (enable-query=false)"
        
        # Create Embed
        embed = discord.Embed(
            title="🔥 Ember Network Status",
            description=f"IP: `{MINECRAFT_IP}`",
            color=discord.Color.orange()
        )
        embed.add_field(name="🟢 Status", value="Online ✅", inline=True)
        embed.add_field(name="📡 Latency", value=f"{status.latency} ms", inline=True)
        embed.add_field(name="👥 Players", value=f"{status.players.online}/{status.players.max}", inline=True)
        embed.add_field(name="🎮 Player List", value=player_names, inline=False)
        embed.set_footer(text="Powered by Ember Network Bot")

        await ctx.send(embed=embed)

    except Exception:
        embed = discord.Embed(
            title="❌ Ember Network Status",
            description=f"IP: `{MINECRAFT_IP}`\nServer is offline or unreachable.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

# --- RUN BOT ---
bot.run(DISCORD_TOKEN)
