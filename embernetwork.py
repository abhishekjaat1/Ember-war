import discord
from discord.ext import commands, tasks
from mcstatus import MinecraftServer

DISCORD_TOKEN = "YOUR_DISCORD_BOT_TOKEN"
PREFIX = "!"
MINECRAFT_IP = "play.yourserver.com" 
MINECRAFT_PORT = 25565

intents = discord.Intents.default()
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f"✅ {bot.user} is online!")
    update_status.start()  

@tasks.loop(seconds=60)  
async def update_status():
    try:
        server = MinecraftServer.lookup(f"{MINECRAFT_IP}:{MINECRAFT_PORT}")
        status = server.status()
        activity = discord.Game(name=f"Ember Network – {status.players.online}/{status.players.max} online")
    except Exception:
        activity = discord.Game(name="Ember Network – Offline ❌")
    
    await bot.change_presence(activity=activity)

@bot.command()
async def status(ctx):
    try:
        server = MinecraftServer.lookup(f"{MINECRAFT_IP}:{MINECRAFT_PORT}")
        
        # Get server status
        status = server.status()

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

bot.run(DISCORD_TOKEN)
