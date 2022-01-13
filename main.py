import discord
from discord.ext import commands
import time
import os
import random
from discord import *
import requests
import json
client = commands.Bot(command_prefix="?")
client.remove_command("help")
E = discord.Embed
light_blue = 0x03b6fc
red = 0xfc030b
green = 0x02e64a\


def opendbb():
  with open("inv.json") as f:
    data = json.load(f)
  return data
def savedb(data):
  with open("inv.json", "w+") as f:
    json.dump(data, f)
def createaccount(ID):

  database = opendbb()
  if ID in database:
    return 
  else:
    database[ID] = {}
    database[ID]["points"] = 0
    savedb(database)
  return

  
@client.event
async def on_ready():
  print(f"Logged in as {client.user}!")



@client.command()
async def create(ctx):
  ID = str(ctx.message.author.id)
  database = opendbb()
  if ID not in database:
    createaccount(ID)
    embed=E(title=f"Created Account!", description=f"{ctx.message.author} Your account has been created!", color=green)
    await ctx.send(embed=embed)
    return
  else:
    embed=E(title=f"Creation Error", description=f"It looks like you already have an account!", color=red)
    await ctx.send(embed=embed)
    return

@client.command()
async def bal(ctx):
  ID = str(ctx.message.author.id)
  createaccount(ID)
  database = opendbb()
  balance = database[ID]["points"]
  msg = ""
  if int(balance) < 5:
    msg = "YOU BROKE"
  else:
    msg = "YOU RICH"
  embed=E(title=f"{ctx.message.author}'s Balance", description=f"Your Point Balance: **{balance}**", color=light_blue)
  embed.set_footer(text=msg)
  await ctx.send(embed=embed)
  return
@client.command()
async def tip(ctx, recviver: discord.Member=None, amount:int=None):
  if recviver == None:
    embed=E(title=f"Tip Command Error", description=f"You did not specify a user to tip!", color=red)
    await ctx.send(embed=embed)
    return
  if recviver.id == ctx.message.author.id:
    embed=E(title=f"Command Error", description=f"You cannot tip yourself!", color=red)
    await ctx.send(embed=embed)
    return
  if amount == None:
    embed=E(title=f"Command Error", description=f"You must specify an amount to tip!", color=red)
    await ctx.send(embed=embed)
    return
  recvID = str(recviver.id)
  ID = str(ctx.message.author.id)
  database = opendbb()
  if ID not in database:
    embed=E(title=f"Command Error", description=f"You do not have a account run the **?create** command to create your account!", color=red)
    await ctx.send(embed=embed)
    return
  if recvID not in database:
    emebd=E(title=f"Error Tipping User", description=f"The user you tried tipping does not have an account!", color=red)
    await ctx.send(embed=emebd)
    return 
  if amount <= 0:
    embed=E(title=f"Tip Error!", description=f"Cannot Tip NULL or Negative amounts!", color=red)
    await ctx.send(embed=embed)
    return
  users_points = database[ID]["points"]
  users_points = int(users_points)
  if int(users_points) < int(amount):
    embed=E(title=f"Transaction Error", description=f"{ctx.message.author} It looks like you do not have enough points to make this transaction!", color=red)
    await ctx.send(embed=embed)
    return
  else:
    try:
      database[ID]["points"] -= int(amount)
      savedb(database)
      database[recvID]["points"] += int(amount)
      savedb(database)
      
    except:
      await ctx.send('Something went wrong!')
      return
    embed=E(title=f"Transaction Proccesed!", description=f"You have sent {amount} to <@{recvID}>", color=green)
    await ctx.send(embed=embed)
    return
  

@client.command()
async def bin(ctx, cc: str=None):
  if cc == None:
    embed=E(title=f"Command Usage Error", description=f"You did not provide the first 6 digits of a cc!", color=red)
    await ctx.send(embed=embed)
    return
  if len(cc) > 6 or len(cc) < 6:
    embed=E(title=f"Command Usage Error", description=f"You did not provide the first 6 numbers on the cc!", color=red)
    await ctx.send(embed=embed)
    return
  try:
    cc = int(cc)
  except Exception:
    embed=E(title=f"Usage Error!", description=f"Seems like you did not provide numbers!", color=red)
    await ctx.send(embed=embed)
    return
  req = requests.get(f"https://lookup.binlist.net/{cc}")
  try:
    json_format = req.json()
    cc_length = json_format["number"]["length"]
    cc_luhn = json_format["number"]["luhn"]
    cc_company_type = json_format["scheme"]
    cc_type = json_format["type"]
    cc_brand = json_format["brand"]
    cc_prepaid = json_format["prepaid"]
  except Exception:
    embed=E(title=f"Something went wrong!", description=f"Looks like you did not provide a valid bin!", color=red)
    await ctx.send(embed=embed)
    return 
  embed=E(title=f"Bin Information", description=f"**Card Length: {cc_length}\n\nLuhn: {cc_luhn}\n\nCard Company: {cc_company_type}\n\nCard Type: {cc_type}\n\nCard Level: {cc_brand}\n\nCard Prepaid: {cc_prepaid}**", color=green)
  embed.set_footer(text="Bandz = Daddy ;)")
  await ctx.send(embed=embed)

  

@client.command()
async def help(ctx):
  embed=E(title="Main Market Bot Commands", description="?help: displays this message\n\n?bin (first 4 digits of card): Returns BIN information about card\n\n", color=light_blue)
  embed.set_footer(text="Bandz = Daddy ;)")
  await ctx.send(embed=embed)




token = os.environ["bottoken"]
client.run(token)
