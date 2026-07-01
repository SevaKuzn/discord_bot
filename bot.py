import discord
import os
import random
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'Бот {bot.user} успешно запустился!')
    print(f'ID бота: {bot.user.id}')
    print('Загруженные команды:', [cmd.name for cmd in bot.commands])

@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f'Задержка: {latency} мс')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Привет, {ctx.author.mention}! Рад тебя видеть! ')

@bot.command()
async def say(ctx, *, message):
    await ctx.send(message)
    try:
        await ctx.message.delete() 
    except:
        pass

@bot.command()
async def help(ctx):
    """Показывает список всех команд бота"""
    
    embed = discord.Embed(
        description="Все мои команды",
        color=discord.Color.blue()
    )

    for command in sorted(bot.commands, key=lambda x: x.name):
        embed.add_field(
            name=f"!{command.name}",
            value=description,
            inline=False
        )
    await ctx.send(embed=embed)

@bot.command()
async def roll(ctx, *args):
    if len(args) == 0:
        min_val = 1
        max_val = 100
    elif len(args) == 1:
        try:
            max_val = int(args[0])
            min_val = 1
            if max_val < 1:
                await ctx.send("Максимальное число должно быть больше 0")
                return
        except ValueError:
            await ctx.send("Неправильный формат! Используй: `!roll [мин] [макс]`")
            return

    elif len(args) == 2:
        try:
            min_val = int(args[0])
            max_val = int(args[1])
            if min_val > max_val:
                await ctx.send("Минимальное число должно быть меньше максимального!")
                return
        except ValueError:
            await ctx.send("Неправильный формат! Используй: `!roll [мин] [макс]`")
            return

    else:
        await ctx.send("Слишком много аргументов! Используй: `!roll [мин] [макс]`")
        return
    
    result = random.randint(min_val, max_val)
    
    await ctx.send(f"Выпало: **{result}**")

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        voice_client = ctx.guild.voice_client 

        if voice_client and voice_client.is_connected():
            await voice_client.move_to(channel)
            await ctx.send(f'Перешел в канал: **{channel.name}**')
        else:
            await channel.connect()
            await ctx.send(f'Подключился к голосовому каналу: **{channel.name}**')
    else:
        await ctx.send('Вы не находитесь в голосовом канале!')

@bot.command()
async def leave(ctx):
    voice_client = ctx.guild.voice_client
    
    if voice_client and voice_client.is_connected():
        await voice_client.disconnect()
        await ctx.send('Отключился от голосового канала')
    else:
        await ctx.send('Бот и так не подключен к голосовому каналу!')

if __name__ == '__main__':
    TOKEN = os.environ.get('DISCORD_TOKEN')
    bot.run(TOKEN)
