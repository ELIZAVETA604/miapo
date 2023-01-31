import discord          
from discord.ext import commands
import os
import sqlite3
from ast import alias
import string
import json

from youtube_dl import YoutubeDL
from music_cog import music_cog
from image_cog import image_cog

bot = commands.Bot(command_prefix='!', intents= discord.Intents.all())

@bot.event
async def on_ready():
    print('Ready') 
    #музыка
    await bot.add_cog(music_cog(bot))
    #картинки
    await bot.add_cog(image_cog(bot))

    global base, cur
    base = sqlite3.connect('Hamster.db')
    cur = base.cursor()
    if base:
        print('DataBase connected')

#команда теста работы бота
@bot.command() 
async def ping(ctx):
    await ctx.send('pong...')

#реакция на присоединение
@bot.event
async def on_member_join(member):
    await member.send('Ура, новый друг! Привет, я бот Хома, рад приветствовать. Просмотр команд - !help')

    for q in bot.get_guild(member.guild.id).channels:
        if q.name == 'основной':
            await bot.get_channel(q.id).send(f'{member}, я рад что ты присоединился к нам, написал тебе лично<3')

#реакция на выход пользователя
@bot.event
async def on_member_remove(member):
    for q in bot.get_guild(member.guild.id).channels:
        if q.name == 'основной':
            await bot.get_channel(q.id).send(f'{member}, мне будет тебя не хватать')

#команда информации о возможностях бота
@bot.command()
async def info(ctx, arg = None):
    author = ctx.message.author
    if arg == None:
        await ctx.send(f'{author.mention} Введите:\n!info main\n!info comm')
    elif arg == 'main':
        await ctx.send(f'{author.mention} Я бэйби хомячок:3 Мне приятно познакомиться с тобой и, надеюсь, ты - дружелюбный. За запретные слова я дам предупреждение. 3 предупреждения = БАН о_0')
    elif arg == 'comm':
        await ctx.send(f'{author.mention} !ping - моя любимая игрушка: Ping Pong\n !status - количество подзатыльников т_т\n !play <url>- проигрывание музыки\n !leave - перестану транслировать музыку\n !pause - поставлю музыку на паузу\n !resume - возобновлю текущую музыку\n !skip - пропуск музыки из очереди\n !queue - очередь из песен\n !clear - очистка очереди\n !get - рандомная пикча')
    else:
        await ctx.send(f'{author.mention} прости, дружочек, но такого я еще не выучил....')

#команда для чата с ботом
@bot.command()
async def как(ctx, arg = None):
    author = ctx.message.author
    if arg == 'дела':
        await ctx.send(f'Покушал, поел и я с вами, конечно же хорошо. А у тебя? {author.mention} ?')
    elif arg == 'здоровье':
         await ctx.send(f'Я кушаю витаминки и пью водичку с лимоном, здоровый как бык, хи-хи. А как у тебя, {author.mention} ?')
    elif arg == 'спалось':
         await ctx.send(f'Спать-спать-спаааать, обожаю, люблю хорошенько выспаться. А тебе,друг {author.mention} ?')
    elif arg == 'жизнь':
         await ctx.send(f'У хомячка жизнь неплоха! У меня всегда весело, когда я не один. А как у тебя, {author.mention} ?')
    elif arg == 'семушки':
         await ctx.send(f'Вкусные жаренные семечки - это заряд позитива. А как у тебя, {author.mention} ?')
    else:
         await ctx.send(f'Ты наверное хотел спросить: "как дела, как здоровье, как спалось, как жизнь или как мои семушки?". {author.mention}')

#статус
@bot.command()
async def status(ctx):
    base.execute('CREATE TABLE IF NOT EXISTS {}(userid INT, count INT)'.format(ctx.message.guild.name))
    base.commit()
    warning = cur.execute('SELECT * FROM {} WHERE userid == ?'.format(ctx.message.guild.name)\
        ,(ctx.message.author.id,)).fetchone()
    if warning == None:
        await ctx.send(f'{ctx.message.author.mention}, у вас нет предупреждений')
    else:
        await ctx.send(f'{ctx.message.author.mention}, у вас {warning[1]} предупреждений')

#команда для анализатора сообщений(на мат и запретки в словах)(бан)
@bot.event
async def on_message(message):
    if {i.lower().translate(str.maketrans('','',string.punctuation)) for i in message.content.split(' ')}\
        .intersection(set(json.load(open('zap.json')))) != set():
        await message.channel.send(f'Ай-ай-ай...больно ушкам хомячка.. как тебе не стыдно, {message.author.mention}?')
        await message.delete()

        name = message.guild.name

        base.execute('CREATE TABLE IF NOT EXISTS {}(userid INT, count INT)'.format(name))
        base.commit()

        warning = cur.execute('SELECT * FROM {} WHERE userid == ?'.format(name),(message.author.id,)).fetchone()

        if warning == None:
            cur.execute('INSERT INTO {} VALUES(?, ?)'.format(name),(message.author.id,1))
            base.commit()
            await message.channel.send(f'{message.author.mention}, первое предупреждение')
        elif warning[1] == 1:
            cur.execute('UPDATE {} SET count == ? WHERE userid == ?'.format(name),(2,message.author.id))
            base.commit()
            await message.channel.send(f'{message.author.mention}, первое предупреждение')
        elif warning[1] == 2:
            cur.execute('UPDATE {} SET count == ? WHERE userid == ?'.format(name),(3,message.author.id))
            base.commit()
            await message.channel.send(f'{message.author.mention}, бан(')
            await message.author.ban(reason='Нецензурные выражения')

    await bot.process_commands(message)

bot.run(os.getenv('TOKEN'))