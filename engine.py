#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xpinyin import Pinyin
import downloader
import random
from myspiders import lianjia_spider
import items
import piplines
import pandas as pd
from threading import Thread
import queue
import time




proxy_url='http://www.xicidaili.com/nn/'

domains = [
    'lianjia.com/ershoufang',
    'lianjia.com/loupan'
]

count = 1000

proxies_pagetxt = downloader.downloader(url=proxy_url)
proxy_ip_list = items.get_proxy_iplist(proxies_pagetxt)
del proxies_pagetxt

def get_random_proxies(ip_list=proxy_ip_list):
    ip_list = [ip.strip().lstrip() for ip in ip_list]
    proxy_ip = 'http://' + random.choice(ip_list)
    proxies = {'http': proxy_ip}
    return proxies


def get_citypair(filename):
    pinyin = Pinyin()
    
    f = open('citys.txt', encoding='utf-8')
    citys_list = [i.strip().lstrip() for i in f.readlines()]
    f.close()
    citys_pinyin = [pinyin.get_initials(i, splitter='').lower() for i in citys_list]
    return dict(zip(citys_pinyin, [pinyin.get_pinyin(i, splitter='') for i in citys_list])).items()

def generate_url(city, root='lianjia.com', subdirpre='ershoufang',):
    url = 'https://{city}.{root}/{subdirpre}/'
    return url.format(city=city,root=root,subdirpre=subdirpre,)




def fech_mainpages(urls, myqueue, tag=False, urlsque=None):
    for url in urls:
        if tag:
            if myqueue.full():
                time.sleep(2)
            myqueue.put(downloader.downloader(url))
            urlsque.put(url)
        else:
            if myqueue.full():
                time.sleep(2)
            myqueue.put(downloader.downloader(url))
    return myqueue

def to_infopd(mydic, infos):
    
    if infos is 0:
        infos = pd.DataFrame([mydic])
    else:
        print(infos.shape[0],infos.shape[1])
        infos.append(pd.DataFrame([mydic]))
    return infos

def fech_lianjiainfo_old(spell, brief):
    
    web = u'lianjia'
    old = domains[0]
    old = old.split('/')
    root_url = generate_url(city=brief, root=old[0], subdirpre=old[1])
    home_txt = downloader.downloader(url=root_url, proxies=get_random_proxies())
    
    urls_old = lianjia_spider.get_mainurls_old(home_txt)
    if not urls_old:
        print('爬取失败')
        return False
    mainpages_que = queue.Queue(10)
    mainpages_que.put(home_txt)
    t_mainpage = Thread(target=fech_mainpages, args=(urls_old, mainpages_que,))
    t_mainpage.start()
    print('爬主页，下载主页到队列')
    #info = pd.DataFrame()
    infos = 0
    while t_mainpage.is_alive() or not mainpages_que.empty():
        if not t_mainpage.is_alive() and mainpages_que.empty():
            break
        if mainpages_que.empty():
            time.sleep(2)
        while not mainpages_que.empty():
            main_txt = mainpages_que.get()
            housepages_que = queue.Queue(100)
            houseurls_que = queue.Queue(100)
            houseurls = lianjia_spider.get_houseurls_old(main_txt)
            t_housepage = Thread(target=fech_mainpages, args=(houseurls, housepages_que, True, houseurls_que))
            t_housepage.start()
            print('楼房信息主页：下载中')
            while t_housepage.is_alive() or not housepages_que.empty():
                if not t_housepage.is_alive() and housepages_que.empty():
                    break
                if housepages_que.empty():
                    time.sleep(1)
                if not housepages_que.empty():
                    housepage_txt = housepages_que.get()
                    houseurl = houseurls_que.get()
                    detail = items.get_info_oldhouse(page_txt=housepage_txt, url=houseurl)
                    if detail == False:
                        print('二手房：detail获取失败')
                    else:
                        if infos is 0:
                            infos = pd.DataFrame([detail])
                        else:
                            info = pd.DataFrame([detail])
                            infos = infos.append(info,ignore_index=True)
                    if infos.shape[0] >= count:
                        piplines.write_csv(data=infos, city=spell, web=web, neworold='old')
                        infos = 0
    return piplines.write_csv(data=infos, city=spell, web=web, neworold='old')


def fech_lianjiainfo_new(spell, brief):
    
    web = u'lianjia'
    d = domains[1]
    d = d.split('/')
    root_url = generate_url(city=brief, root=d[0], subdirpre=d[1])
    home_txt = downloader.downloader(url=root_url, proxies=get_random_proxies())
    urls_new = lianjia_spider.get_mainurls_new(home_txt)
    if not urls_new:
        print('爬取失败')
        return False
    infos = 0
    mainpages_que = queue.Queue(100)
    mainpages_que.put(home_txt)
    t_mainpage = Thread(target=fech_mainpages, args=(urls_new, mainpages_que,))
    t_mainpage.start()
    info = pd.DataFrame()
    while t_mainpage.is_alive() or not mainpages_que.empty():
        if not t_mainpage.is_alive() and mainpages_que.empty():
            break
        if mainpages_que.empty():
            time.sleep(2)
        while not mainpages_que.empty():
            
            main_txt = mainpages_que.get()
            housepages_que = queue.Queue(300)
            houseurls_que = queue.Queue(300)
            houseurls = lianjia_spider.get_houseurls_new(main_txt)
            t_housepage = Thread(target=fech_mainpages, args=(houseurls, housepages_que, True, houseurls_que))
            t_housepage.start()
            
            while t_housepage.is_alive() or not housepages_que.empty():
                if not t_housepage.is_alive() and housepages_que.empty():
                    break
                if not housepages_que.empty():
                    housepage_txt = housepages_que.get()
                    houseurl = houseurls_que.get()
                    detail = items.get_info_newhouse(page_txt=housepage_txt, url=houseurl)
                    if detail == False:
                        print('新房获取item失败')
                    else:
                        if infos is 0:
                            infos = pd.DataFrame([detail])
                        else:
                            info = pd.DataFrame([detail])
                            infos = infos.append(info,ignore_index=True)
                    # print('======================')
                    # print('下面是infos：\n')
                    # print(infos)
                    if infos.shape[0]>=count:
                        piplines.write_csv(data=infos, city=spell, web=web, neworold='new')
                        infos = 0
    return piplines.write_csv(data=infos, city=spell, web=web, neworold='new')







