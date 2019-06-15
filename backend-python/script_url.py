#!/usr/bin/python

import json
import os
import requests
import string
import sys


def get_token(streamer_name):
    url = 'https://api.twitch.tv/api/channels/' + streamer_name + '/access_token'
    obj = twitch_api(url)
    return (obj.pop('token'), obj.pop('sig'))

def twitch_api(url):
    url += '?client_id=1ht9oitznxzdo3agmdbn3dydbm06q2'
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

def kappamain(name):
    DATA_PATH = os.path.join(os.getcwd(), name)

    try:
        os.mkdir(DATA_PATH)
    except OSError as e:
        if e.errno != 17:
            print(e)
            raise(e)

    url = parse_stream(name)

    r = requests.get(url)
    r.raise_for_status()
    with open(os.path.join(DATA_PATH, name), 'wb') as f:
        f.write(r.text)
    
    with open(os.path.join(DATA_PATH, name), 'r') as f:
        for str in f:
            if 'http://' in str:
                break

    print(str)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Usage: {} twitch_channel_name')

    try:
        kappamain(sys.argv[1])
    except requests.exceptions.HTTPError as e:
        print(e)
