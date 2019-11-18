#!/usr/bin/env python3
#-*- coding:utf8 -*-
def log(message,file='log.log',echo=True):
    with open(file,'a',encoding='utf-8') as f:
        if echo:
            print(message)
        f.write(message+"\n")
def exception(message):
    log(message,file='Exception.log')