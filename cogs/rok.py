import discord
import asyncio
from discord.ext import commands

class RoKBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ROLE_IDS = {
            "Infantry": 1526342009596547142,
            "Cavalry": 1526341870899298426,
            "Archery": 1526342056430141440,
            "Siege": 1526342109983014942
        }

    # Birlik Seçim Menüsü
    class RoleSelect(discord.ui.Select):
        def __init__(self, role_ids):
            self.role_ids = role_ids
            options = [discord.SelectOption(label=name, value=str(role_id)) for name, role_id in role_ids.items()]
            super().__init__(placeholder="Birlik seçin...", options=options)

        async def callback(self, interaction: discord.Interaction):
            role_id = int(self.values[0])
            role = interaction.guild.get_role(role_id)
            if role:
                await interaction.user.add_roles(role)
                await interaction.response.send_message(f"✅ {role.name} rolü başarıyla verildi!", ephemeral=True)

    class RoleSelectView(discord.ui.View):
        def __init__(self, role_ids):
            super().__init__(timeout=None)
            self.add_item(RoKBot.RoleSelect(role_ids))

    # İsim Değiştirme Modalı
    class NicknameModal(discord.ui.Modal, title='RoK Kayıt Sistemi'):
        isim = discord.ui.TextInput(label='Oyun içi isminiz?', required=True)

        def __init__(self, role_ids):
            super().__init__()
            self.role_ids = role_ids

        async def on_submit(self, interaction: discord.Interaction):
            try:
                await interaction.user.edit(nick=str(self.isim))
                await interaction.response.send_message("Şimdi birliğinizi seçin:", view=RoKBot.RoleSelectView(self.role_ids), ephemeral=True)
            except Exception as e:
                await interaction.response.send_message(f"Bir hata oluştu: {e}", ephemeral=True)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def kayit(self, ctx):
        await ctx.message.delete()
        view = discord.ui.View(timeout=None)
        btn = discord.ui.Button(label="Kaydı Başlat", style=discord.ButtonStyle.primary)
        
        async def btn_callback(interaction: discord.Interaction):
            await interaction.response.send_modal(self.NicknameModal(self.ROLE_IDS))
            
        btn.callback = btn_callback
        view.add_item(btn)
        await ctx.send("Kayıt olmak için aşağıdaki butona tıklayın:", view=view)

async def setup(bot):
    await bot.add_cog(RoKBot(bot))