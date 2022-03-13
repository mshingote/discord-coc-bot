import discord
from keep_alive import keep_alive
from clashofclan import *

client = discord.Client()


@client.event
async def on_ready():
    tag = os.getenv('COC_CLAN_TAG')
    print(f'Clan Tag: {tag}')
    print('!We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith('!!'):
        m = ClashOfClan.get_super_troops_from_clan()
        await message.channel.send(m)


keep_alive()
client.run(os.getenv('TOKEN'))
