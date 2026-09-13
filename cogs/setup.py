#------------imports------------
import discord
from discord import app_commands
from discord.ext import commands
from database import set_admin_role
from database import get_guild
from database import reset_guild_setup
from database import set_role_autocreated
from database import set_modules

#------------/setup------------
class SetupWizardView(discord.ui.View):
    def __init__(self, author: discord.Member):
        super().__init__(timeout=600)
        self.author = author
        self.current_page = 0
        self.admin_role_id = None
        self.enabled_modules = []
    
    def build_page_0(self):
        embed = discord.Embed(
        title="Welcome to glint!",
        description="Welcome to glint, a 100% free, multi purpose discord bot. Click the button below to get started...",
        color=discord.Color.from_str("#2bf0e6")
        
    )
        return embed
    
    @discord.ui.button(label="Get Started!", style=discord.ButtonStyle.green)
    async def get_started_click(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page = 1
        self.show_page_1()
        await interaction.response.edit_message(embed=self.build_page_1(), view=self)
        
    def build_page_1(self):
        embed = discord.Embed(
        title="Choose your administrator role",
        description="Users with this role will be able to configure your bot however they like, this could include enabling potentially disruptive actions, so only give it to people you trust!\nSelect a pre existing role, or Glint can make one for you:",
        color=discord.Color.from_str("#2bf0e6")
        
    )
        return embed
    
    def show_page_1(self):
        self.clear_items()
    
        role_menu = discord.ui.RoleSelect(placeholder="Select your Admin Role...")
        role_menu.callback = self.on_role_selected
    
        role_btn = discord.ui.Button(label="Auto-Create Admin Role", style=discord.ButtonStyle.blurple)
        role_btn.callback = self.on_role_auto_create
    
        self.add_item(role_menu)
        self.add_item(role_btn)

    async def on_role_selected(self, interaction: discord.Interaction):
        selected_roles = interaction.data.get("values", [])
        chosen_id = int(selected_roles[0])
    
        set_admin_role(interaction.guild.id, chosen_id)
    
        self.current_page = 2
        self.clear_items()
        self.show_page_2()
        await interaction.response.edit_message(embed=self.build_page_2(), view=self)
        
    async def on_role_auto_create(self, interaction: discord.Interaction):
        new_role = await interaction.guild.create_role(name="Glint Admin", color=discord.Color.from_str("#2bf0e6"), mentionable=True)
        set_admin_role(interaction.guild.id, new_role.id)
        set_role_autocreated(interaction.guild.id)
    
        self.current_page = 2
        self.clear_items()
        self.show_page_2()
        await interaction.response.edit_message(embed=self.build_page_2(), view=self)
        
    def build_welcome_back(self):
        embed = discord.Embed(
        title="We've detected some previous progress...",
        description="But it's no problem! You can choose whether to continue from where you left off setting Glint up, or start over.",
        color=discord.Color.from_str("#2bf0e6")
    )
        return embed
    
    def show_welcome_back(self):
        self.clear_items()
    
        continue_btn = discord.ui.Button(label="Continue", style=discord.ButtonStyle.green)
        continue_btn.callback = self.on_continue_setup
    
        restart_btn = discord.ui.Button(label="Start Over", style=discord.ButtonStyle.red)
        restart_btn.callback = self.on_restart_setup
    
        self.add_item(continue_btn)
        self.add_item(restart_btn)
    
    async def on_restart_setup(self, interaction: discord.Interaction):
        guild_data = get_guild(interaction.guild.id)
        admin_role_id = guild_data[3]
        auto_created = guild_data[4]
    
        if auto_created == 1:
            role = interaction.guild.get_role(admin_role_id)
            if role:
                await role.delete()
                
        reset_guild_setup(interaction.guild.id)
        
        self.current_page = 1
        self.clear_items()
        new_view = SetupWizardView(self.author)
        new_view.show_page_1()
        await interaction.response.edit_message(embed=new_view.build_page_1(), view=new_view)
        
    async def on_continue_setup(self, interaction: discord.Interaction):
        self.current_page = 2
        self.clear_items()
        self.show_page_2()
        await interaction.response.edit_message(embed=self.build_page_2(), view=self)
        
        
    def build_page_2(self):
        embed = discord.Embed(
        title="What modules would you like?",
        description="Modules are packs of features. Each of said features can be turned off and customised individually. You can have as many or few modules as you like. We know that choice can be overwhelming, but you can change these at any time!",
        color=discord.Color.from_str("#2bf0e6")
        
    )
        return embed
    
    def show_page_2(self):
        self.clear_items()
        
        module_menu = discord.ui.Select(
            placeholder="Select your modules...",
            min_values=1,
            max_values=8,
            options=[
                discord.SelectOption(label="Moderation", value="moderation"),
                discord.SelectOption(label="Moderation (advanced)", value="moderation-advanced"),
                discord.SelectOption(label="Levelling", value="levelling"),
                discord.SelectOption(label="Modmail & Ticketing", value="modmail-ticketing"),
                discord.SelectOption(label="Server security (advanced)", value="server-security-advanced"),
                discord.SelectOption(label="Voice channels", value="voice-channels"),
                discord.SelectOption(label="Socials & Stat tracking", value="socials-stat-tracking"),
                discord.SelectOption(label="Bot Customisation", value="bot-customisation"),
            ]
        )
        module_menu.callback = self.on_module_selected
        self.add_item(module_menu)
        
    async def on_module_selected(self, interaction: discord.Interaction):
        selected_modules = interaction.data.get("values", [])
        set_modules(interaction.guild.id, selected_modules)
        self.clear_items()
        await interaction.response.edit_message(embed=self.build_page_3(), view=self)
    
    def build_page_3(self):
        embed = discord.Embed(
        title="Setup complete!",
        description="Thank you for chosing glint. If you would like to further configure the bot, you can use the /setup command at any time. If you experience any issues, please create a ticket in our support server or use /bug_report!",
        color=discord.Color.from_str("#2bf0e6")
        
    )
        return embed
        
        


#------------setup cog------------
class SetupCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

#------------create setup command------------        
    @app_commands.command(name="setup", description="Begin the tailored Glint configuration flow!")
    async def setup(self, interaction: discord.Interaction):
        guild_data = get_guild(interaction.guild.id)
        admin_role_id = guild_data[3]

        
        if admin_role_id is None:
            view = SetupWizardView(interaction.user)
            await interaction.response.send_message(embed=view.build_page_0(), view=view, ephemeral=True)
        else:

            view = SetupWizardView(interaction.user)
            view.show_welcome_back()
            embed=view.build_welcome_back()
            view=view
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


        




#------------allow load cog from main------------
async def setup(bot):
    await bot.add_cog(SetupCog(bot))
