#!/usr/bin/python

import argparse
import json
import os
import requests
import string
import subprocess
import sys

from pprint import pprint
from pymongo import MongoClient


CLIENTID = '1ht9oitznxzdo3agmdbn3dydbm06q2'
HEADERS = {'Client-ID': CLIENTID}

def reset_cid(data):
  global CLIENTID
  global HEADERS

  CLIENTID = data.cid
  HEADERS['Client-ID'] = CLIENTID

def get_user_by_name(streamer_name):
  global HEADERS

  r = requests.get('https://api.twitch.tv/helix/users?login={}'.format(streamer_name), headers=HEADERS)
  r.raise_for_status()
  data = r.json()

  if len(data['data']) != 1:
    raise()

  return data['data'][0]

def get_latest_vod_by_uid(uid):
  global HEADERS

  r = requests.get('https://api.twitch.tv/helix/videos?user_id={}&type={}&first=1'.format(uid, 'archive'), headers=HEADERS)
  r.raise_for_status()
  data = r.json()
  return data['data'][0]

def get_token(streamer_name):
  url = 'https://api.twitch.tv/api/channels/' + streamer_name + '/access_token'
  obj = twitch_api(url)
  pprint(obj)
  return (obj.pop('token'), obj.pop('sig'))

def twitch_api(url):
  global CLIENTID

  url += '?client_id={}'.format(CLIENTID)
  r = requests.get(url)
  r.raise_for_status()
  return r.json()

def parse_stream(streamer_name):
  token, sig = get_token(streamer_name)
  streamer_url = 'http://usher.twitch.tv/api/channel/hls/' + streamer_name + '.m3u8'
  streamer_url += '?player=twitchweb'
  streamer_url += '&token=' + token
  streamer_url += '&sig=' + sig
  streamer_url += '&allow_audio_only=true&allow_source=true&type=any'
  return streamer_url

def kappamain(conf):
  name = conf.twitch_name
  fps = conf.fps
  reset_cid(conf)

  DATA_PATH = os.path.join(os.getcwd(), 'data', name)

  try:
    os.mkdir(DATA_PATH)
  except OSError as e:
    if e.errno != 17:
      print(e)
      raise(e)

  url = parse_stream(name)

  r = requests.get(url)
  r.raise_for_status()
  with open(os.path.join(DATA_PATH, 'url.txt'), 'wb') as f:
    f.write(r.content)

  with open(os.path.join(DATA_PATH, 'url.txt'), 'r') as f:
    for str in f:
      if 'http://' in str:
        break
  
  # DB
  db = MongoClient('localhost', 27017).schoolcv

  # API stuff
  user = db.streamers.find_one({'name': name})
  if not user:
    # user = get_user_by_name(name)
    user = {u'broadcaster_type': u'partner',
              u'description': u'',
              u'display_name': u'GodHunt',
              u'id': u'28295429',
              u'login': u'godhunt',
              u'offline_image_url': u'https://static-cdn.jtvnw.net/jtv_user_pictures/557bf3a9-c76a-4b6e-81f1-d564664f68f2-channel_offline_image-1920x1080.png',
              u'profile_image_url': u'https://static-cdn.jtvnw.net/jtv_user_pictures/godhunt-profile_image-edf107addd3d4dbc-300x300.jpeg',
              u'type': u'',
              u'view_count': 11027064}
    user['_id'] = user['id']
    try:
      db.streamers.replace_one(user, upsert=True)
    except Exception as e:
      print(e)

  # vod = get_latest_vod_by_uid(user['id'])
  vod = {u'created_at': u'2019-06-16T04:39:53Z',
            u'description': u'',
            u'duration': u'2h11m10s',
            u'id': u'439750626',
            u'language': u'ru',
            u'published_at': u'2019-06-16T04:39:53Z',
            u'thumbnail_url': u'',
            u'title': u'RU\U0001f534 IG vs  Royal  | FVL   by GodHunt  ',
            u'type': u'archive',
            u'url': u'https://www.twitch.tv/videos/439750626',
            u'user_id': u'28295429',
            u'user_name': u'GodHunt',
            u'view_count': 7,
            u'viewable': u'public'}

  # FFMPEG get screenshot
  str = str.rstrip()
  callarr = ['ffmpeg', '-i', str, '-vf', 'fps={}'.format(fps), '-t', '00:00:01', '{}/{}_%d.png'.format(DATA_PATH, vod['id'])]
  print(' '.join(callarr))
  subprocess.call(callarr)

  # Prepare images
  RESULT_PATH = os.path.join(os.getcwd(), 'result', name)
  callarr = ['python', './detector/face_align.py', '--source_root', DATA_PATH, '--dest_root', RESULT_PATH]
  print(' '.join(callarr))
  subprocess.call(callarr)

  # Process images
  callarr = ['python', './recognition/recognize.py', '--root', RESULT_PATH, '--vod', vod['id']]
  print(' '.join(callarr))
  subprocess.call(callarr)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Fetches twitch streams as screenshots')
  parser.add_argument('twitch_name', type=str, help='Stream name which will be fetched')
  parser.add_argument('--fps', default='1', type=str, help='Requested FPS')
  parser.add_argument('--cid', type=str, required=True, help='Twitch API app client ID')

  conf = parser.parse_args()

  try:
    kappamain(conf)
  except requests.exceptions.HTTPError as e:
    print(e)
