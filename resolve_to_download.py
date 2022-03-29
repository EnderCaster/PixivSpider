#!/usr/bin/env python3
#-*- coding:utf8 -*-
from AimImages import AimImages
import argparse
import os
import download_util

arg_parser=argparse.ArgumentParser()
arg_parser.add_argument('csv_name_without_csv')
arg_parser.add_argument("--dir",default="./",help="download base dir")
args=arg_parser.parse_args()
file_name=args.csv_name_without_csv
download_dir=os.path.abspath(args.dir)

already_exists=[]
already_exists_ids=[]
with open(file_name+'.csv','r',encoding='utf-8') as f:
    image=AimImages()
    line=f.readline()
    while line!=None and len(line)>0:
        image.load(line)
        download_util.download_directly(image.url,download_dir)
        line=f.readline()
