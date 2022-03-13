import os
import json
import requests
import logging


class ClashOfClan:
    apis = {
        'members': 'https://api.clashofclans.com/v1/clans/%s/members',
        'player': 'https://api.clashofclans.com/v1/players/%s',
    }

    @staticmethod
    def get_members(clan_tag=None):
        if clan_tag is None:
            clan_tag = os.getenv('COC_CLAN_TAG')
            assert clan_tag is not None, 'Empty clan tag'
        token = os.getenv('COC_TOKEN')
        assert token is not None, 'Empty api token'
        headers = {
            'clanTag': clan_tag,
            'authorization': "Bearer %s" % token,
        }

        try:
            url = ClashOfClan.apis['members'] % clan_tag.replace("#", "%23")
            response = requests.request("GET", url, headers=headers)
            parsed_response = json.loads(response.text)
            return parsed_response.get('items', None)
        except Exception as e:
            logging.exception(e)

    @staticmethod
    def get_super_troops(player_tag=None):
        troops = ClashOfClan.get_troops(player_tag)
        if troops is None:
            logging.error('Failed to get super troop info')
            return
        super_troops = []
        for troop in troops:
            if 'superTroopIsActive' in troop:
                super_troops.append(troop['name'])
        return super_troops

    @staticmethod
    def get_super_troops_from_clan(clan_tag=None):
        members = ClashOfClan.get_members(clan_tag)
        all_super_troops = []
        if members is None:
            logging.error('Failed to get all super troops from clan')
            return
        for member in members:
            if type(member) is not dict:
                continue
            player_tag = member.get('tag', None)
            if player_tag is None:
                logging.info('Failed to get player tag')
                continue
            player_name = member.get('name', None)
            if player_name is None:
                logging.info(f'Failed to get player name for {player_tag}')
                continue
            super_troops = ClashOfClan.get_super_troops(player_tag)
            if super_troops is None:
                logging.error(f'Failed to get super troops for {player_tag}')
                continue
            if len(super_troops) == 0:
                continue
            super_troops = {
                'player_name': player_name,
                'player_tag': player_tag,
                'super_troops': super_troops
            }
            all_super_troops.append(super_troops)
        return all_super_troops

    @staticmethod
    def get_troops(player_tag=None):
        if player_tag is None:
            player_tag = os.getenv('COC_PLAYER_TAG')
            assert player_tag is not None, 'Empty player tag'

        token = os.getenv('COC_TOKEN')
        assert token is not None, 'Empty api token'

        headers = {
            'playerTag': player_tag,
            'authorization': "Bearer %s" % token,
        }

        try:
            url = ClashOfClan.apis['player'] % player_tag.replace("#", "%23")
            response = requests.request("GET", url, headers=headers)
            player_info = json.loads(response.text)
            troops = player_info.get('troops', None)
            if troops is None:
                logging.error(response)
                return
            return troops
        except Exception as e:
            logging.exception(e)


if __name__ == '__main__':
    import sys

    print(f'python version={sys.version}')
    print(f'Current file={__file__}')

    ip = requests.get('https://api.ipify.org').content.decode('utf8')
    print('My public IP address is: {}'.format(ip))

    from dotenv import load_dotenv

    load_dotenv(".env")

    print(f'clan_tag={os.getenv("COC_CLAN_TAG")}')
    print(f'player_tag={os.getenv("COC_PLAYER_TAG")}')
    print(f'coc_token={os.getenv("COC_TOKEN")}')

    members = ClashOfClan.get_members()
    print(f'members = {members}')

    troops = ClashOfClan.get_troops()
    print(f'troops = {troops}')

    super_troops = ClashOfClan.get_super_troops()
    print(f'super_troops = {super_troops}')

    all_super_troops = ClashOfClan.get_super_troops_from_clan()
    print(f'all_super_troops = {all_super_troops}')
