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
                f.write(",".join(self.table_header)+"\n")

        with open(file_name,"a",encoding='utf-8') as record:
            record.write(",".join(line)+"\n")
    