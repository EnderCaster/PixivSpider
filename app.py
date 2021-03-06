#!/usr/bin/env python3
#-*- coding:utf8 -*-
import requests as req
import time
from AimImages import AimImages
from random import random
import argparse
from urllib import parse
import json
from Log import log
from Log import exception
import os
from Settings import *

arg_parser=argparse.ArgumentParser()
arg_parser.add_argument('keyword')
arg_parser.add_argument("--min-width",default=0,help="The minium width of the image")
arg_parser.add_argument("--min-height",default=0,help="The minium height of the image")
arg_parser.add_argument("--ratio",help="WIDTH:HEIGHT What ratio of the image you want")
arg_parser.add_argument("--start-page",default=0,help="start page")

args=arg_parser.parse_args()
keyword=parse.quote(args.keyword)
exists_file_name=parse.unquote(keyword)+'-already_exists_ids.txt'
url_file_name=parse.unquote(keyword)+'-already_exists.txt'
already_exists=[]
if not os.path.exists(exists_file_name):
    log('parsing start',exists_file_name)

with open(exists_file_name,'r') as f:
    line=f.readline().strip()
    while len(line)>0:
        if not line in already_exists:
            already_exists.append(line)
        line=f.readline().strip()
    
    

base_url="https://www.pixiv.net/ajax/search/artworks/"+keyword+"?word="+keyword
headers={
    "Connection":"close",
    "user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
    "x-user-id":HEADER_USER_ID,
    "cookie":HEADER_COOKIES,
    "referer":"https://www.pixiv.net/tags/"+keyword+"/artworks?s_mode=s_tag",
    'authority':'www.pixiv.net',
    'pragma':'no-cache',
    'cache-control': 'no-cache',
    'accept': 'application/json',
    'dnt': '1',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'accept-encoding': 'gzip, deflate, br'
    }
index_count=int(args.start_page)
start_url=base_url
if(index_count>0):
    start_url=start_url+"&p="+str(index_count-1)
resp=req.get(base_url,headers=headers)
temp=0
while resp:
    page=index_count+1
    log('Now,parsing page '+str(page))
    resp_json=json.loads(resp.text)
    data=[]
    if not resp_json['error']:
        data=resp_json['body']['illustManga']['data']
    if len(data) <= 0:
        break
    # need refer header when download curl -e 'https://www.pixiv.net/'
    for image_profile in data:
        try:
            if image_profile['id'] in already_exists:
                continue
            if len(data) <= 0:
                break
            if args.min_height and args.min_height > image_profile['height']:
                continue
            if args.min_width and args.min_width > image_profile['width']:
                continue
            if args.ratio:
                width,height=args.ratio.split(':')
                if width*image_profile['height'] != height*image_profile['width']:
                    continue
            request_url="https://www.pixiv.net/ajax/illust/"+image_profile['id']+"/pages"
            log('Now,parsing illust: '+image_profile['id']+'-'+image_profile['title'])
            resp_image_post=req.get(request_url,headers=headers)
            illust_json=json.loads(resp_image_post.text)
            illusts=[]
            if not illust_json['error']:
                illusts=illust_json['body']
            
            for illust in illusts:
                image=AimImages(keyword=parse.unquote(keyword))
                image.id=image_profile['id']
                image.title=image_profile['title']
                image.source="https://www.pixiv.net/artworks/"+image_profile['id']
                image.tags=",".join(image_profile['tags'])
                image.author=image_profile['userName']
                image.author_id=image_profile['userId']
                image.url=illust['urls']['original']
                image.save()
                log(illust['urls']['original'] ,file=url_file_name,echo=False)
                
            already_exists.append(image_profile['id'])
            log(image_profile['id'] ,file=exists_file_name,echo=False)
        except Exception as e:
            exception("Exception:"+str(e))
            if "id" in image_profile.keys():
                log(str(image_profile),parse.unquote(keyword)+'-failed_images.txt')
            else:
                exception("image_profile:"+str(image_profile))
        except KeyboardInterrupt as ki:
            log(str(page),'EndAt.txt')
            exit()
        
    index_count=page
    next_url=base_url+"&p="+str(page+1)

    resp=req.get(next_url,headers=headers)
