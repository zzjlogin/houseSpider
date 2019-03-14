#!/usr/bin/env python
# -*- coding: utf-8 -*-

import downloader
from myspiders import spider_anjuke
import pandas as pd
from items import items_anjuke
import piplines

def generate_mainurl(url='https://sjz.anjuke.com/sale/'):
    urls = []
    for i in range(1,51):
        urls.append(url+'p'+str(i))
    return urls


def fech_anjuke_old():
    
    for url in generate_mainurl():
        print(url)
        mainpage_txt = downloader.downloader(url)
        
        houseurls = spider_anjuke.get_houseurls_old(mainpage_txt)
        infos = pd.DataFrame()
        for houseurl in houseurls:
            housepage_txt = downloader.downloader(houseurl)
            infos.append(pd.DataFrame([items_anjuke.get_items_old(housepage_txt,houseurl)]))
    
    piplines.write_csv(data=infos,city='shijiazhuang',web='anjuke',)

fech_anjuke_old()