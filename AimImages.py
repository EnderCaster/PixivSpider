#!/usr/bin/env python3
#-*- coding:utf8 -*-
class AimImages:
    def __init__(self,keyword='record'):
        self.table_header=['ID','Title','Source','Tag List','Author ID','Author','URL']
        self.id=''
        self.title=''
        self.source=''
        self.tags=''
        self.author=''
        self.author_id=''
        self.url=''
        self.url_file_name=keyword
        self.url_file_extension='.csv'
    def save(self):
        line=[]
        line.append(self.id)
        line.append(self.title)
        line.append(self.source)
        line.append(self.tags)
        line.append(self.author_id)
        line.append(self.author)
        line.append(self.url)
        file_name=self.url_file_name+self.url_file_extension

        import os
        if not os.path.exists(file_name):
            with open(file_name,'w',encoding='utf-8') as f:
                f.write("\t".join(self.table_header)+"\n")

        with open(file_name,"a",encoding='utf-8') as record:
            record.write("\t".join(line)+"\n")
    def load(self,line):
        line=line.strip()
        if len(line)<=0:
            self.url=''
            return 
        params=line.split("\t")
        self.id=params[0]
        self.title=params[1]
        self.source=params[2]
        self.tags=params[3]
        self.author_id=params[4]
        self.author=params[5]
        self.url=params[6]
