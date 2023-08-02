import discord
import asyncio
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.voice_states = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Глобальные переменные
user_id = USER_ID # int
guild_id = guild_id # int
voice_clients = {}  # Словарь для хранения голосовых клиентов для каждого сервера
audio_file_path = 'audio_file_path'  # Путь к аудиофайлу

async def play_audio(voice_channel):
    voice_client = voice_channel.guild.voice_client
    if not voice_client:
        voice_client = await voice_channel.connect()
        voice_clients[voice_channel.guild.id] = voice_client

    voice_client.play(discord.FFmpegPCMAudio(audio_file_path), after=None)

async def repeat_play_audio(voice_channel):
    while True:
        await asyncio.sleep(5)  # Ожидание 5 секунд перед повторным проигрыванием
        voice_client = voice_clients.get(voice_channel.guild.id)
        if voice_client and not voice_client.is_playing():
            voice_client.play(discord.FFmpegPCMAudio(audio_file_path), after=None)

@bot.event
async def on_ready():
    guild = bot.get_guild(guild_id)
    if guild:
        user = guild.get_member(user_id)
        if user and user.voice and user.voice.channel:
            await play_audio(user.voice.channel)
            await repeat_play_audio(user.voice.channel)

@bot.event
async def on_voice_state_update(member, before, after):
    if member.id == user_id:
        if after.channel:
            # Пользователь переместился на другой канал
            if member.guild.id in voice_clients and after.channel != voice_clients[member.guild.id].channel:
                await voice_clients[member.guild.id].disconnect()
            await play_audio(after.channel)
        else:
            # Пользователь вышел из голосового канала, отключаем бота
            if member.guild.id in voice_clients:
                await voice_clients[member.guild.id].disconnect()

async def run_bot():
    TOKEN = 'DS_BOT_TOKEN'
    await bot.start(TOKEN)

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(run_bot())
except KeyboardInterrupt:
    loop.run_until_complete(bot.close())
finally:
    loop.close()
