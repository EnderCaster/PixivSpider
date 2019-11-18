#!/usr/bin/env python3
#-*- coding:utf8 -*-
from AimImages import AimImages
import argparse

arg_parser=argparse.ArgumentParser()
arg_parser.add_argument('csv_name_without_csv')
args=arg_parser.parse_args()
file_name=args.csv_name_without_csv
already_exists=[]
with open(file_name+'.csv','r',encoding='utf-8') as f:
    image=AimImages()
    line=f.readline()
    while line!=None and len(line)>0:
        image.load(line)
        if image.url.startswith('http') and not image.url in already_exists:
            already_exists.append(image.url)
        line=f.readline()
    

with open('already_exists.txt','a',encoding='utf-8') as f:
    f.write("\n".join(already_exists))
