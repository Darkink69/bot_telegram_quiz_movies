import random
import subprocess
import os
from pymongo import MongoClient
import yt_dlp_info
import json


# client = MongoClient('mongodb://localhost:27017/')
# db = client['urldb']
# collection = db['mongourls']
# items = collection.find()

def get_film(date):

    with open('soviet_movies.json', 'r', encoding='utf-8') as f:
        items = json.load(f)

    list_links = []
    for item in items:
        list_links.append(item)

    for film in range(1):

        print(random.choice(list_links)['url'])

        try:
            info = yt_dlp_info.get_info_dlp(random.choice(list_links)['url'])
        except BaseException:
            print('yt_dlp не сработал :( Надо попробовать позже..')

        print(info['title'])
        print(info['duration'])
        # print(info['description'])
        # print(info)
        id = info['id']

        for i in info['formats']:
            if i['format_id'] == '18':
                # prev_video['url_medium'] = i['url']
                link = i['url']


        for i in range(1):
            rnd_sec = random.randrange(info['duration'])
            print(rnd_sec)
            pro = f'ffmpeg -i "{link}" -ss {rnd_sec // (60 * 60)}:{rnd_sec // 60 - 60 if (rnd_sec // 60) >= 60 else rnd_sec // 60}:{rnd_sec % 60} -frames:v 1 out/{date}_{id}_{i}.png'
            print(pro)
            pr = subprocess.run(pro, shell=True, stdin=None, stderr=subprocess.PIPE)

            return f'{date}_{id}_{i}.png', info['title']
