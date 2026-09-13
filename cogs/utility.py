#------------imports------------
import discord
from discord import app_commands
from discord.ext import commands
import hashlib
import os


    




#------------setup cog------------
class UtilityCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

#------------create hash_verify command------------        
    @app_commands.command(name="hash_verify", description="Verify the file hash (advanced)")
    async def hash_verify(self, interaction: discord.Interaction):
        
        embed = discord.Embed(
            title="File hash",
            description="Here at glint, we know that security is important, and want to give you peace of mind. While all of our code is open sourced on GitHub, how can you know that we are using that same code? This /command returns a SHA-256 hash of all the bot's files, so you can match and verify them to our GitHub files...",
            color=discord.Color.from_str("#2bf0e6")
        
        )
    
        results = []
        for folder, subfolders, files in os.walk("."):
            for filename in files:
                if filename.endswith(".env") or filename.endswith(".md"):
                    continue
                filepath = os.path.join(folder, filename)
                with open(filepath, "rb") as f:
                    file_hash = hashlib.sha256(f.read()).hexdigest()
                results.append((filepath, file_hash))
                
        for filepath, file_hash in results:
            embed.add_field(name=filepath, value=file_hash, inline=False)
            
        await interaction.response.send_message(embed=embed, ephemeral=True)

        

#------------allow load cog from main------------
async def setup(bot):
    await bot.add_cog(UtilityCog(bot))