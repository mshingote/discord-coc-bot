import os
import json
import discord
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

def coc_get_members(url):
    try:
        headers = {
            'clantag': os.getenv('CLAN_TAG'),
            'authorization': "Bearer %s" % os.getenv('CC'),
            'cache-control': "no-cache",
            'postman-token': "71b8a4a7-1001-ed24-3335-54f692471829"
        }
        response = requests.request("GET", url, headers=headers)
        return json.loads(response.text)
    except Exception as e:
        print(e)


def coc_get_super_troops(url, player_tag):
    try:
        headers = {
            'playerTag': player_tag,
            'authorization': "Bearer %s" % os.getenv('CC'),
            'cache-control': "no-cache",
            'postman-token': "71b8a4a7-1001-ed24-3335-54f692471829"
        }
        response = requests.request("GET", url, headers=headers)
        player_info = json.loads(response.text)
        troops = player_info['troops']
        names = []
        #print(f'{player_tag} has {len(troops)}')
        for troop in troops:
            #print(troop.keys())
            if 'superTroopIsActive' in troop:
                names.append(troop['name'])
                #print(names[-1])
        return sorted(names)
    except Exception as e:
        print(e)


def main():
    tag = os.getenv('CLAN_TAG')
    print(f'Clan Tag: {tag}')
    clan_url = "https://api.clashofclans.com/v1/clans/%s/members" % (tag.replace("#", "%23"))
    items = coc_get_members(clan_url)
    s = set()
    msg = []
    #print(items)
    for i in range(len(items['items'])):
        player = items['items'][i]
        tag = player.get('tag', "")
        name = player.get('name', "")
        player_url = "https://api.clashofclans.com/v1/players/%s" % (tag.replace("#", "%23"))
        troops = coc_get_super_troops(player_url, tag)
        #print(troops)
        if troops:
            #print((f'{name} ==> {troops}'))
            msg.append(f'{name} has {troops}')
            print(msg[-1])
            s.update(troops)
    if s:
        msg.append(f'Unique super troops are : {s}')
    return msg

client = discord.Client()

@client.event
async def on_ready():
  
  tag = os.getenv('CLAN_TAG')
  print(f'Clan Tag: {tag}')
  print('!We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith('!!'):
    print('got msg!')
    m=main()
    m.append("")
    m.append("")
    m.append("~ bot by storm!")
    m="\n".join(m)
    
    await message.channel.send(m)

keep_alive()
client.run(os.getenv('TOKEN'))
