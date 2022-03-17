import discord
from tabulate import tabulate
from cachetools import TTLCache

from keep_alive import keep_alive
from clashofclan import *

client = discord.Client()


@client.event
async def on_ready():
    tag = os.getenv('COC_CLAN_TAG')
    print(f'Clan Tag: {tag}')
    print('!We have logged in as {0.user}'.format(client))

cache = TTLCache(maxsize=1024*1024, ttl=600)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content.strip()
    if msg.startswith('#'):
        if len(msg) > 11:
            return
        
        def get_cache_troops(msg):
            global cache
            if msg in cache:
                return cache[msg]
            troops = ClashOfClan.get_super_troops_from_clan(msg)
            cache[msg] =troops
            return troops
        
        try:
            troops = get_cache_troops(msg)
            formatted_msg = tabulate(troops)
            formatted_msg = f"```{formatted_msg}```"
            print(formatted_msg)
            await message.channel.send(formatted_msg)
        except Exception as e:
            logging.exception(f'msg={msg}, e={e}')

keep_alive()
client.run(os.getenv('TOKEN'))
