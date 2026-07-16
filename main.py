import discord
import os
import asyncio
from discord.ext import commands
from flask import Flask
from threading import Thread

# Web sunucusu (7/24 aktiflik için)
app = Flask('')
@app.route('/')
def home(): return "Bot aktif!"
Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.reactions = True

bot = commands.Bot(command_prefix="!", intents=intents)

async def load_extensions():
    # cogs klasöründeki tüm .py dosyalarını yükle
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

async def main():
    async with bot:
        await load_extensions()
        await bot.start(os.environ.get('DISCORD_BOT_TOKEN'))

if __name__ == '__main__':
    asyncio.run(main())