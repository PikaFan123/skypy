
#######################################
#                                     #
#  Hypixel Skyblock API Wrapper v0.1  #
#                                     #
#   by: Jordan Baron Copyright 2019   #  
#                                     #
#######################################




import requests
import json
from bs4 import BeautifulSoup

# ---------------- EXCEPTIONS ----------------

base_url = 'https://api.hypixel.net'
api_key = ''

class InvalidUsernameError(Exception):
  pass

class InvalidUUIDError(Exception):
  pass

class InvalidAPIKeyError(Exception):
  pass

# --------------------------------------------

class Skyblock():

  def __init__(self, key):
    self.api_key = key

  def set_api_key(self, key):
    self.api_key = key

  def uname_resolver(self, uname):
    try:
      req = requests.get('https://api.mojang.com/users/profiles/minecraft/' + uname).content
      return json.loads(req)['id']
    except KeyError:
      raise InvalidUsernameError

  def uuid_resolver(self, uuid):
    try:
      req = requests.get('https://api.mojang.com/user/profiles/' + uuid + '/names').content
      return json.loads(req)[-1]['name']
    except KeyError:
      raise InvalidUUIDError

  def __call_api(self, endpoint, reqtype='get'):

    if not self.api_key:
      raise InvalidAPIKeyError

    # build endpoint url
    endpoint_url = base_url
    
    if '?' in endpoint:
      endpoint_url += endpoint + '&key=' + self.api_key
    else:
      endpoint_url += endpoint + '?key=' + self.api_key

    # send request
    resp = requests.get(endpoint_url).content
    resp = json.loads(resp)

    # check if invalid api key
    if resp['success'] == False and resp['cause'] == 'Invalid API key!':
      raise InvalidAPIKeyError

    return resp

  def is_player_online(self, player):
    player_data = self.__call_api('/player?name=' + player)['player']
    return player_data['lastLogout'] < player_data['lastLogin']

  def get_news(self):
    news = {}
    data = self.__call_api('/skyblock/news')
    url = data['items'][0]['link']
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    post = soup.find('blockquote')
    news['news'] = post
    return news
  
  def get_player_profiles(self, uuid=None, player=None):
    if uuid is not None:
        profiles = {}
        player = self.__call_api('/player?uuid=' + uuid)
        profile_ids = player['player']['stats']['SkyBlock']['profiles']

        for k,v in profile_ids.items():
          profiles[v['cute_name']] = k

        return profiles
    else:
        suuid = self.uname_resolver(player)
        profiles = {}
        player = self.__call_api('/player?uuid=' + suuid)
        profile_ids = player['player']['stats']['SkyBlock']['profiles']

        for k,v in profile_ids.items():
          profiles[v['cute_name']] = k

        return profiles

  
  def get_player_auctions(self, uuid, profiles, pn=0, page=1):
    profile = list(profiles.values())[pn]
    resp = self.__call_api('/skyblock/auction?uuid=' + uuid + '&profile=' + profile)
