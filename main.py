import discord
from discord.ext import commands
import time
import os
import random
from discord import *
import requests
import json
client = commands.Bot(command_prefix="?") # bot prefix
client.remove_command("help") # removes orginal help embed
E = discord.Embed # Im hella lazy so I asigned discord.Embed as E so I don't gotta type more
light_blue = 0x03b6fc # Hex Color Value for Blue
red = 0xfc030b # Hex color Value for Red
green = 0x02e64a # Hex color Value for Red
@client.event
async def on_ready():
  print(f"Logged in as {client.user}!") # on bot startup 


@client.command() # on ?bin command
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

  

@client.command() # new help command 
async def help(ctx):
  embed=E(title="Main Market Bot Commands", description="?help: displays this message\n\n?bin (first 4 digits of card): Returns BIN information about card\n\n", color=light_blue)
  embed.set_footer(text="Bandz = Daddy ;)")
  await ctx.send(embed=embed)




token = "bot token" # DO NOT SHARE THIS sharing this can allow other people to have full access on your bot
client.run(token) # runs the bot
