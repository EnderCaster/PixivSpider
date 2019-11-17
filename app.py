#!/usr/bin/env python3
#-*- coding:utf8 -*-
import requests as req
import time
from SETTINGS import SETTINGS
from AimImages import AimImages
from random import random
import argparse
from urllib import parse
import json

arg_parser=argparse.ArgumentParser()
arg_parser.add_argument('keyword')
args=arg_parser.parse_args()
keyword=parse.quote(args.keyword)

start_url="https://www.pixiv.net/ajax/search/artworks/"+keyword+"?word="+keyword
headers={"Connection":"close"}
resp=req.get(start_url)
index_count=0

temp=0
while resp:
    resp_json=json.loads(resp.text)
    data=[]
    if not resp_json['error']:
        data=resp_json['body']['illustManga']['data']
    if len(data) <= 0:
        break
    # need refer header when download curl -e 'https://www.pixiv.net/'
    for image_profile in data:
        request_url="https://www.pixiv.net/ajax/illust/"+image_profile['illustId']+"/pages"
        resp_image_post=req.get(request_url,headers=headers)
        illust_json=json.loads(resp_image_post.text)
        illusts=[]
        if not illust_json['error']:
            illusts=illust_json['body']
        if len(data) <= 0:
            break
        for illust in illusts:
            print(illusts)
            image=AimImages(keyword=parse.unquote(keyword))
            image.id=image_profile['id']
            image.title=image_profile['illustTitle']
            image.source="https://www.pixiv.net/artworks/"+image_profile['id']
            image.tags="    ".join(image_profile['tags'])
            image.author=image_profile['userName']
            image.author_id=image_profile['userId']
            image.url=illust['urls']['original']
            image.save()
        # time.sleep(SETTINGS.DELAY_BASE+3*random())
        exit()
        
    index_count+=1
    page=index_count
    next_url=start_url+"&p="+str(page)

    resp=req.get(next_url)
