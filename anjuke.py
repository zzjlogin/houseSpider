#!/usr/bin/env python
# -*- coding: utf-8 -*-

import downloader
from myspiders import spider_anjuke
import pandas as pd
from items import items_anjuke
import piplines
import random


proxy_url = 'http://www.xicidaili.com/nn/'
try:
    #this is test
    proxies_pagetxt = downloader.downloader(url=proxy_url)
    proxy_ip_list = items_lianjia.get_proxy_iplist(proxies_pagetxt)
except:
    proxy_ip_list = []
del proxies_pagetxt



def get_random_proxies(ip_list=proxy_ip_list):
    # print('执行：get_random_proxies')
    if ip_list == []:
        return None
    ip_list = [ip.strip().lstrip() for ip in ip_list]
    proxy_ip = 'http://' + random.choice(ip_list)
    proxies = {'http': proxy_ip}
    return proxies

def generate_mainurl(url='https://sjz.anjuke.com/sale/'):
    urls = []
    for i in range(1,51):
        urls.append(url+'p'+str(i))
    return urls


def fech_anjuke_old():
    
    for url in generate_mainurl():
        print(url)
        mainpage_txt = downloader.downloader(url,proxies=get_random_proxies())
        
        houseurls = spider_anjuke.get_houseurls_old(mainpage_txt)
        infos = pd.DataFrame()
        for houseurl in houseurls:
            housepage_txt = downloader.downloader(houseurl, proxies=get_random_proxies())
            if housepage_txt is False:
                pass
            else:
                info = items_anjuke.get_items_old(housepage_txt,houseurl)
                if info is False:
                    pass
                else:
                    info = pd.DataFrame([info])
                    infos = infos.append(info, ignore_index=True)
    
        piplines.write_csv(data=infos,city='shijiazhuang',web='anjuke',)
        infos = pd.DataFrame()

fech_anjuke_old()