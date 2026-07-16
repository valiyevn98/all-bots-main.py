import discord
from discord.ext import commands
from discord.ui import Select, View, Button

# Senin Discord ID'n (Bildirimlerin buraya gelmesi için)
MY_ID = 980764213683314739 

class SteamBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.GAMES = [
            "Call of Duty: Modern Warfare", "Cyberpunk 2077", "Detroit: Become Human",
            "Dying Light", "EA SPORTS FC 25", "Elden Ring", "Frostpunk", "God of War",
            "God of War Ragnarök", "Marvel’s Spider-Man: Miles Morales", "Resident Evil Village",
            "Resident Evil 4", "Red Dead Redemption 2", "Rise of the Tomb Raider",
            "Shadow of the Tomb Raider", "Sons of the Forest", "The Last of Us part 1",
            "The Last of Us part 2", "The Witcher 3: Wild Hunt", "Tomb Raider"
        ]

    # Oyun seçim menüsünü oluşturan sınıf
    class GameSelect(Select):
        def __init__(self, games):
            options = [discord.SelectOption(label=game) for game in games]
            super().__init__(placeholder="Oyun seç...", options=options)

        async def callback(self, interaction: discord.Interaction):
            await interaction.response.send_message("✅ Seçiminiz alındı, yöneticimize iletildi.", ephemeral=True)
            
            # Sahibine DM atma
            owner = await interaction.client.fetch_user(MY_ID)
            if owner:
                embed = discord.Embed(title="🛒 Yeni Satış Talebi!", color=discord.Color.gold())
                embed.add_field(name="👤 Kullanıcı", value=f"{interaction.user.mention}", inline=False)
                embed.add_field(name="🎮 Seçilen Oyun", value=self.values[0], inline=False)
                
                view = View()
                view.add_item(Button(label="Kullanıcıya Mesaj At", url=f"https://discord.com/users/{interaction.user.id}"))
                await owner.send(embed=embed, view=view)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def oyunlar(self, ctx):
        await ctx.message.delete()
        view = View(timeout=None)
        view.add_item(self.GameSelect(self.GAMES))
        
        embed = discord.Embed(
            title="Oyun Satın Alma Listesi",
            description="Aşağıdaki menüden almak istediğiniz oyunu seçin.",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(SteamBot(bot))