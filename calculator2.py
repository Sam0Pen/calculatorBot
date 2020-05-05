import random
import discord
from discord.ext import commands
from datetime import date
import sqlite3
import functools

conn = sqlite3.connect("my_database.db")
cursor = conn.cursor()

#getting a date and making it show in right format
today = date.today()
d1 = today.strftime("%d/%m/%Y")

TOKEN = ""

bot = commands.Bot(command_prefix='!', description='Wacky bot.')



@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

#command to import outcomes of the day
@bot.command()
async def insert(ctx, a: int):
    sql = "INSERT INTO OUTCOME (date, sum) VALUES (?, ?)"
    cursor.execute(sql, [(d1), (a)])
    conn.commit()
    await ctx.send('Amount inserted')

#command to see sum of outcome of one day
@bot.command()
async def open(ctx, a: str):
    sql = "SELECT sum FROM OUTCOME WHERE date = ?"
    cursor.execute(sql, [(a)])
    y = cursor.fetchall()
    conn.commit()
    z = 0
    for x in y:
        #converting tuple to int
        res = int(''.join(map(str, x))) 
        z = z + int(res)
    await ctx.send(z)

#command to delete one day
@bot.command()
async def delete(ctx, a: str):
    sql = "DELETE FROM OUTCOME WHERE date = ?"
    cursor.execute(sql, [(a)])
    conn.commit()
    await ctx.send("Day is deleted")

#command to see what day it is
@bot.command()
async def date(ctx):
    await ctx.send(d1)

#basic calculator commands
@bot.command()
async def add(ctx, a: float, b: float):
    await ctx.send(a+b)

@bot.command()
async def multiply(ctx, a: float, b: float):
    await ctx.send(a*b)

@bot.command()
async def division(ctx, a: float, b: float):
    await ctx.send(a/b)

@bot.command()
async def minus(ctx, a: float, b: float):
    await ctx.send(a-b)

#removing default help command and making own after that
bot.remove_command('help')

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Calculator", description="List of wacky commands are:", color=0xeee657)

    embed.add_field(name="!date", value="Gives todays date", inline=False)
    embed.add_field(name="!insert X", value="Saves new outcome for this day", inline=False)
    embed.add_field(name="!open xx/xx/xxxx", value="Shows the sum of that specific day", inline=False)
    embed.add_field(name="!delete xx/xx/xxxx", value="Delete outcomes of specific day", inline=False)
    embed.add_field(name="!add X Y", value="Gives the addition of **X** and **Y**", inline=False)
    embed.add_field(name="!multiply X Y", value="Gives the multiplication of **X** and **Y**", inline=False)
    embed.add_field(name="!division X Y", value="Gives the division of **X** and **Y**", inline=False)
    embed.add_field(name="!minus X Y", value="Gives the difference of **X** and **Y**", inline=False)
    await ctx.send(embed=embed)


bot.run(TOKEN)