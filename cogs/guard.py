import discord
import asyncio
from discord.ext import commands

class Guard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Orijinal dosyanızdaki bekleme listesini buraya taşıdık
        self.bekleme_listesi = {}

    async def bekleme_suresi(self, user_id):
        # 7200 saniye = 2 saat
        await asyncio.sleep(7200)
        if user_id in self.bekleme_listesi:
            del self.bekleme_listesi[user_id]
            print(f"ID: {user_id} bekleme süresi doldu.")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        # Eğer zaten listedeyse eski görevi iptal et, yenisini başlat
        if member.id in self.bekleme_listesi:
            self.bekleme_listesi[member.id].cancel()
        
        gorev = asyncio.create_task(self.bekleme_suresi(member.id))
        self.bekleme_listesi[member.id] = gorev
        print(f"{member.name} sunucudan çıktı, 2 saatlik koruma başladı.")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # Kullanıcı katılınca listede var mı diye bak
        if member.id in self.bekleme_listesi:
            try:
                await member.send("Sunucuya tekrar girmek için 2 saatlik süren dolmadı.")
                await member.kick(reason="2 saatlik yeniden giriş bekleme süresi dolmadı.")
                print(f"{member.name} 2 saat dolmadan girdiği için atıldı.")
            except discord.Forbidden:
                print(f"{member.name} atılamadı, yetkim yok.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def affet(self, ctx, user_id: int):
        await ctx.message.delete()
        if user_id in self.bekleme_listesi:
            self.bekleme_listesi[user_id].cancel()
            del self.bekleme_listesi[user_id]
            await ctx.send(f"✅ {user_id} ID'li kullanıcı manuel olarak affedildi.", delete_after=5)
        else:
            await ctx.send("❌ Bu kullanıcı zaten bekleme listesinde değil.", delete_after=5)

# Bu kısım botun bu dosyayı bir modül olarak tanımasını sağlar
async def setup(bot):
    await bot.add_cog(Guard(bot))