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

arg_parser=argparse.ArgumentParser()
arg_parser.add_argument('keyword')
arg_parser.add_argument("--min-width",default=0,help="The minium width of the image")
arg_parser.add_argument("--min-height",default=0,help="The minium height of the image")
arg_parser.add_argument("--ratio",dest="WIDTH:HEIGHT",help="What ratio of the image you want")
arg_parser.add_argument("--start-page",default=0,help="start page")

args=arg_parser.parse_args()
keyword=parse.quote(args.keyword)
exists_file_name='already_exists.txt'
already_exists=[]
if not os.path.exists(exists_file_name):
    log('file created',exists_file_name)

with open(exists_file_name,'r') as f:
    line=f.readline().strip()
    while len(line)>0:
        if not line in already_exists:
            already_exists.append(line)
        line=f.readline().strip()
    
    


start_url="https://www.pixiv.net/ajax/search/artworks/"+keyword+"?word="+keyword
headers={"Connection":"close"}
resp=req.get(start_url)
index_count=args.start_page

temp=0
while resp:
    log('Now,parsing page '+str(index_count+1))
    resp_json=json.loads(resp.text)
    data=[]
    if not resp_json['error']:
        data=resp_json['body']['illustManga']['data']
    if len(data) <= 0:
        break
    # need refer header when download curl -e 'https://www.pixiv.net/'
    for image_profile in data:
        try:
            if args.min_height and args.min_height > image_profile['height']:
                continue
            if args.min_width and args.min_width > image_profile['width']:
                continue
            if args.ratio:
                width,height=args.ratio.split(':')
                if width*image_profile['height'] != height*image_profile['width']:
                    continue
            request_url="https://www.pixiv.net/ajax/illust/"+image_profile['illustId']+"/pages"
            log('Now,parsing illust: '+image_profile['illustId']+'-'+image_profile['illustTitle'])
            resp_image_post=req.get(request_url,headers=headers)
            illust_json=json.loads(resp_image_post.text)
            illusts=[]
            if not illust_json['error']:
                illusts=illust_json['body']
            if len(data) <= 0:
                break
            for illust in illusts:
                if illust['urls']['original'] in already_exists:
                    continue
                image=AimImages(keyword=parse.unquote(keyword))
                image.id=image_profile['id']
                image.title=image_profile['illustTitle']
                image.source="https://www.pixiv.net/artworks/"+image_profile['id']
                image.tags=",".join(image_profile['tags'])
                image.author=image_profile['userName']
                image.author_id=image_profile['userId']
                image.url=illust['urls']['original']
                image.save()
                already_exists.append(illust['urls']['original'])
                log(illust['urls']['original'],file=exists_file_name,echo=False)
        except Exception as e:
            exception("Exception:"+str(e))
            exception("image_profile:"+str(image_profile)+"\n")
        except KeyboardInterrupt as ki:
            log(str(index_count+1),'EndAt')
            exit()
        
    index_count+=1
    page=index_count
    next_url=start_url+"&p="+str(page)

    resp=req.get(next_url)
