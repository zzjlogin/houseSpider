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
    'lianjia.com/loufang'
]

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


pagetxt_queue = queue.Queue(100)

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
    return True

def fech_lianjiainfo(spell, brief):
    info_detail = 0
    web = u'lianjia'
    for d in domains:
        print(d)
        d = d.split('/')
        print(d)
        root_url = generate_url(city=brief, root=d[0], subdirpre=d[1])
        home_txt = downloader.downloader(url=root_url, proxies=get_random_proxies())
        
        urls_old = lianjia_spider.get_mainurls_old(home_txt)
        if not urls_old:
            print('爬取失败')
            return False
        mainpages_que = queue.Queue(100)
        mainpages_que.put(home_txt)
        t_mainpage = Thread(target=fech_mainpages, args=(urls_old, mainpages_que,))
        t_mainpage.start()
        info = pd.DataFrame()
        while t_mainpage.is_alive() or not mainpages_que.empty():
            while t_mainpage.is_alive() and mainpages_que.empty():
                time.sleep(1)
            main_txt = pagetxt_queue.get()
            housepages_que = queue.Queue(100)
            houseurls_que = queue.Queue(100)
            houseurls = lianjia_spider.get_houseurls_old(main_txt)
            t_housepage = Thread(target=fech_mainpages, args=(houseurls, housepages_que, True, houseurls_que))
            t_housepage.start()
            
            while t_housepage.is_alive() or not housepages_que.empty():
                while t_housepage.is_alive() and housepages_que.empty():
                    time.sleep(1)
                housepage_txt = housepages_que.get()
                houseurl = houseurls_que.get()
                detail = items.get_info(page_txt=housepage_txt, url=houseurl)
                if detail == False:
                    pass
                info = pd.DataFrame([detail])
            if info.shape[0] >= 10000:
                piplines.write_csv(data=info, city=spell, web=web, neworold='old')
        return piplines.write_csv(data=info, city=spell, web=web, neworold='old')


def fech_lianjiainfo_new(spell, brief):
    info_detail = 0
    web = u'lianjia'
    for d in domains:
        d = d.split('/')
        print(d[0] + 'd1:'+d[1])
        root_url = generate_url(city=brief, root=d[0], subdirpre=d[1])
        home_txt = downloader.downloader(url=root_url, proxies=get_random_proxies())
        
        urls_new = lianjia_spider.get_mainurls_new(home_txt)
        if not urls_new:
            print('爬取失败')
            return False
        mainpages_que = queue.Queue(100)
        mainpages_que.put(home_txt)
        t_mainpage = Thread(target=fech_mainpages, args=(urls_new, mainpages_que,))
        t_mainpage.start()
        info = pd.DataFrame()
        while t_mainpage.is_alive() or not mainpages_que.empty():
            while t_mainpage.is_alive() and mainpages_que.empty():
                time.sleep(1)
            main_txt = pagetxt_queue.get()
            housepages_que = queue.Queue(100)
            houseurls_que = queue.Queue(100)
            houseurls = lianjia_spider.get_houseurls_new(main_txt)
            t_housepage = Thread(target=fech_mainpages, args=(houseurls, housepages_que, True, houseurls_que))
            t_housepage.start()
            
            while t_housepage.is_alive() or not housepages_que.empty():
                while t_housepage.is_alive() and housepages_que.empty():
                    time.sleep(1)
                housepage_txt = housepages_que.get()
                houseurl = houseurls_que.get()
                detail = items.get_info(page_txt=housepage_txt, url=houseurl)
                if detail == False:
                    pass
                info = pd.DataFrame([detail])
            if info.shape[0]>=10000:
                piplines.write_csv(data=info, city=spell, web=web, neworold='new')
        return piplines.write_csv(data=info, city=spell, web=web, neworold='new')







