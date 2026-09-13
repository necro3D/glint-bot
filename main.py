#------------imports------------
import os
import asyncio
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from database import initialize_db
from database import add_guild

#------------intents------------
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="g!", intents=intents)



#------------load token------------
load_dotenv('secrets.env')
TOKEN = os.getenv('DISCORD_TOKEN')

#------------load necessary cogs------------
async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            cog_name = filename[:-3]
            await bot.load_extension(f'cogs.{cog_name}')
            print(f"Loaded extension: {cog_name}")
            


#------------run bot------------
@bot.event
async def setup_hook():
    initialize_db()
    await load_extensions()

async def main():
    async with bot:
        await bot.start(TOKEN)

@bot.event
async def on_guild_join(guild):
    add_guild(guild.id, guild.name)
    
        

#------------sync with test server------------

@bot.event
async def on_ready():
    print(f"Success! Glint is online and logged in as {bot.user}")
    
    for guild in bot.guilds:
        add_guild(guild.id, guild.name)
        #IMPORTANT: PLACEHOLDER
        bot.tree.copy_global_to(guild=discord.Object(id=guild.id))
        print(bot.tree.get_commands(guild=discord.Object(id=guild.id)))
        await bot.tree.sync(guild=discord.Object(id=guild.id))
        print(f"Synced commands for {guild.name}")

        
#------------run async------------
if __name__ == "__main__":
    asyncio.run(main())







