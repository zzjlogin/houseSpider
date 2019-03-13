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

proxy_url = 'http://www.xicidaili.com/nn/'
try:
    
    proxies_pagetxt = downloader.downloader(url=proxy_url)
    proxy_ip_list = items.get_proxy_iplist(proxies_pagetxt)
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




domains = [
    'lianjia.com/ershoufang',
    'lianjia.com/loupan'
]

count = 1000



def get_citypair(filename):
    pinyin = Pinyin()
    f = open(filename, encoding='utf-8')
    citys_list = [i.strip().lstrip() for i in f.readlines()]
    f.close()
    citys_pinyin = [pinyin.get_initials(i, splitter='',).lower() for i in citys_list]
    return dict(zip(citys_pinyin, [pinyin.get_pinyin(i, splitter='') for i in citys_list])).items()

def generate_url(city, root='lianjia.com', subdirpre='ershoufang',):
    url = 'https://{city}.{root}/{subdirpre}/'
    return url.format(city=city,root=root,subdirpre=subdirpre,)

def fech_pages(mylist, myqueue, tag=False, que1=None):
    # print('执行：fech_pages')
    for num_i in mylist:
        # print('把这个url的页面压入队列： ' + num_i)
        if tag:
            while myqueue.full():
                time.sleep(2)
            url_page = downloader.downloader(num_i, proxies=get_random_proxies(),)
            if url_page == False:
                pass
            else:
                myqueue.put(url_page)
                que1.put(num_i)
        else:
            while myqueue.full():
                time.sleep(10)
            url_page = downloader.downloader(num_i, proxies=get_random_proxies(),)
            if url_page == False:
                pass
            else:
                myqueue.put(url_page)
    return True

def get_questatus(que, t,):
    #print('执行：get_questatus')
    if not t.is_alive() and que.empty():
        return True
    else:
        return False

def que_map_fuc(que1, que2, fun, t, tag=0, que3=None,):
    # print('执行：que_map_fuc')
    if tag == 0:
        '''
        此时que1中每个元素，用fun处理后压入que2
        '''
        if get_questatus(que=que1, t=t,):
            return True
        while not get_questatus(que=que1, t=t):
            while que2.full():
                time.sleep(1)
            temp = fun(que1.get())
            que2.put(temp)
    elif tag == 1:
        '''
        此时que2中每个元素是迭代器，循环que1中迭代器中每个元素用fun处理
        '''
        if get_questatus(que=que1, t=t):
            return True
        while not get_questatus(que=que1, t=t):
            while que2.full():
                time.sleep(1)
            temp = que1.get()
            temp = fun(temp)
            for i in temp:
                # print('正在压入que2：' + i)
                while que2.full():
                    time.sleep(1)
                que2.put(i)
                # print('成功压入que2：' + i)
    elif tag == 2:
        '''
        此时que1中每个元素，用fun处理后压入que2
        并把每个元素压入que3
        '''
        if get_questatus(que=que1, t=t,):
            return True
        while not get_questatus(que=que1, t=t):
            while que2.full():
                time.sleep(1)
            temp = que1.get()
            que2.put(fun(temp))
            que3.put(temp)
    return True

def to_infopd(mydic, infos):
    # print('执行：to_infopd')
    if infos is 0:
        infos = pd.DataFrame([mydic])
    else:
        infos.append(pd.DataFrame([mydic]))
    return infos

def fech_lianjiainfo_old(spell, brief):
    # print('执行：fech_lianjiainfo_old')
    web = u'lianjia'
    old = domains[0]
    old = old.split('/')
    root_url = generate_url(city=brief, root=old[0], subdirpre=old[1])
    home_txt = downloader.downloader(url=root_url, proxies=get_random_proxies())
    
    mainurls_old = lianjia_spider.get_mainurls_old(home_txt)

    if not mainurls_old:
        print('爬取首页失败')
        return False
    mainpages_que = queue.Queue(10)
    mainpages_que.put(home_txt)
    t_mainpage = Thread(target=fech_pages, args=(mainurls_old, mainpages_que,))
    # print('开始爬取主页面，1-100页主页下载中（二手房）')
    t_mainpage.start()
    # print('爬主页，下载主页到队列')
    infos = pd.DataFrame()
    houseurls_que1 = queue.Queue(300)
    t_houseurls = Thread(target=que_map_fuc, args=(mainpages_que,
                                                   houseurls_que1,
                                                   lianjia_spider.get_houseurls_old,
                                                   t_mainpage,
                                                   1))
    t_houseurls.start()
    # print('开始爬取mainpage中的所有二手房子url，并压入队列')
    housepages_que = queue.Queue(300)
    houseurls_que2 = queue.Queue(300)
    t_housepages = Thread(target=que_map_fuc, args=(houseurls_que1,
                                                    housepages_que,
                                                    downloader.downloader,
                                                    t_houseurls,
                                                    2,
                                                    houseurls_que2))
    t_housepages.start()
    
    while not get_questatus(que=housepages_que, t=t_housepages):
        
        # print('mainpage页面是否为空：'+str(mainpages_que.empty()))
        # print('t_mainpage状态:'+str(t_mainpage.is_alive()))
        # print('houseurls_que1是否为空：'+str(houseurls_que1.empty()))
        # print('t_houseurls状态:' + str(t_houseurls.is_alive()))
        #
        # print('housepages_que是否为空：'+str(housepages_que.empty()))
        # print('t_housepages状态：'+ str(t_housepages.is_alive()))
        while not housepages_que.empty():
            print('楼房信息主页：housepages_que，不为空，分析信息中.....')
    
            housepage_txt = housepages_que.get()
            houseurl = houseurls_que2.get()
            print('分析二手房主页url的page页面：'+houseurl)
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
                infos = pd.DataFrame()
            # print("===================================================================================")
            # print(infos.shape[0])
        else:
            time.sleep(10)
    return piplines.write_csv(data=infos, city=spell, web=web, neworold='old')


def fech_lianjiainfo_new(spell, brief):
    # print('执行：fech_lianjiainfo_new')
    web = u'lianjia'
    new = domains[1]
    new = new.split('/')
    root_url = generate_url(city=brief, root=new[0], subdirpre=new[1])
    # print('新房主页url：'+root_url)
    home_txt = downloader.downloader(url=root_url, proxies=get_random_proxies())
    
    mainurls_new = lianjia_spider.get_mainurls_new(home_txt)
    
    if not mainurls_new:
        print('爬取首页失败')
        return False
    mainpages_que = queue.Queue(10)
    mainpages_que.put(home_txt)
    
    t_mainpage = Thread(target=fech_pages, args=(mainurls_new, mainpages_que,))
    # print('开始爬取主页面，1-xxx页主页下载中（新房）')
    t_mainpage.start()
    # print('爬主页，下载主页到队列')
    infos = pd.DataFrame()
    houseurls_que1 = queue.Queue(300)
    t_houseurls = Thread(target=que_map_fuc, args=(mainpages_que,
                                                   houseurls_que1,
                                                   lianjia_spider.get_houseurls_new,
                                                   t_mainpage,
                                                   1))
    t_houseurls.start()
    # print('开始爬取mainpage中的所有新房子url，并压入队列')
    housepages_que = queue.Queue(300)
    houseurls_que2 = queue.Queue(300)
    t_housepages = Thread(target=que_map_fuc, args=(houseurls_que1,
                                                    housepages_que,
                                                    downloader.downloader,
                                                    t_houseurls,
                                                    2,
                                                    houseurls_que2))
    t_housepages.start()
    
    while not get_questatus(que=housepages_que, t=t_housepages):
        
        # print('mainpage页面是否为空：\t' + str(mainpages_que.empty()))
        # print('t_mainpage状态：\t' + str(t_mainpage.is_alive()))
        # print('houseurls_que1是否为空：\t' + str(houseurls_que1.empty()))
        # print('t_houseurls状态：\t' + str(t_houseurls.is_alive()))
        #
        # print('housepages_que是否为空：\t' + str(housepages_que.empty()))
        # print('t_housepages状态：\t' + str(t_housepages.is_alive()))
        while not housepages_que.empty():
            # print('楼房信息主页：housepages_que，不为空，分析信息中.....')
            
            housepage_txt = housepages_que.get()
            houseurl = houseurls_que2.get()
            # print('分析新房主页url的page页面：' + houseurl)
            detail = items.get_info_newhouse(page_txt=housepage_txt, url=houseurl)
            if detail == False:
                print('新房：detail获取失败')
            else:
                if infos is 0:
                    infos = pd.DataFrame([detail])
                else:
                    info = pd.DataFrame([detail])
                    infos = infos.append(info, ignore_index=True)
            if infos.shape[0] >= count:
                piplines.write_csv(data=infos, city=spell, web=web, neworold='new')
                infos = pd.DataFrame()
            # print("===================================================================================")
            # print(infos.shape[0])
        else:
            time.sleep(10)
    return piplines.write_csv(data=infos, city=spell, web=web, neworold='new')






