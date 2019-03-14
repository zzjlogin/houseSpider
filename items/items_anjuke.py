#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import datetime



def get_items_old(page_txt, url):
    print('获取二手房item信息：' + url)
    info = {}
    soup = BeautifulSoup(page_txt, 'lxml')
    try:
        
        info['title'] = soup.select('.long-title')[0].text.strip()
        #soup.select('.clearfix')[0].text.strip()
    except:
        info['title'] = ''
    try:
        info['totalprice'] = soup.select('.light')[0].next.text.strip()
    except:
        info['totalprice'] = ''
    try:
        info['persquaremeterprice'] = soup.select('.houseInfo-content')[2].text.strip()
    except:
        info['persquaremeterprice'] = ''
    try:
        info['totalarea'] = soup.select('.houseInfo-content')[4].text.strip().strip(u'平方米')
        # info['villagename_lianjia'] = soup.select('.label')[0].next.next.text
    except:
        info['totalarea'] = ''
    try:
        info['villagename'] = soup.select('.houseInfo-content')[0].text.strip()
    except:
        info['villagename'] = ''
    try:
        info['district'] = soup.select('.houseInfo-content')[3].text.strip()
    except:
        info['district'] = ''
    try:
        info['housetype'] = soup.select('.houseInfo-content')[9].text.strip()
    except:
        info['housetype'] = ''
    try:
        info['floor'] = soup.select('.houseInfo-content')[10].text.strip()
    except:
        info['floor'] = ''
    try:
        info['buildtime'] = soup.select('.houseInfo-content')[6].text.strip()
    except:
        info['buildtime'] = ''
    try:
        info['publishtime'] = soup.select('.house-encode')[0].next.next.next
    except:
        info['publishtime'] = ''
    for i, j in info.items():
        if j is not '':
            info['url'] = url
            info['recordtime'] = datetime.datetime.now().isoformat()
            return info

    print('新房：获取信息失败，url：' + url)
    return False

