# This is a asynchronous wrapper for Hori-API named `aiohoripy`

## The way you use it it's so simple:
```py
import aiohoripy
# or 
from aiohoripy import sfw, nsfw

import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="prefix", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("I'm ready")

@bot.command()
async def waifu(ctx):
    image = await sfw(tag="waifu")
    # or
    image = await nsfw(tag="waifu")
    await ctx.send(image)

bot.run("TOKEN")
```
The tags are the same as the tags that the api gives

sfw tags are: `["all", "husbando", "waifu"]`

nsfw tags are: `["ass", "ecchi", "ero", "hentai", "maid", "milf", "oppai", "oral", "paizuri", "selfies", "uniform"]`

The output that` `image`` gives is the same as the json results in the API

and you can get them with:

`image["code", "is_over18", "tag_id", "tag_name", "file", "url"]`

# Made by lvlahraam#8435
