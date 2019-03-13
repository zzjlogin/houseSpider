#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import datetime



def get_info_old_58(page_txt, url):
    print('获取二手房item信息：' + url)
    info = {}
    try:
        soup = BeautifulSoup(page_txt, 'lxml')
        info['title'] = soup.select('.house-title')[0].next.next.text
        info['totalprice'] = ''
        info['persquaremeterprice'] = soup.select('.unitPriceValue')[0].next
        info['totalarea'] = soup.select('.area')[0].next.next.strip(u'平米')
        # info['villagename_lianjia'] = soup.select('.label')[0].next.next.text
        info['villagename'] = soup.select('.info')[0].text
        info['district'] = soup.select('.info')[1].next.text
        info['housetype'] = soup.select('.base')[0].select('.label')[0].next.next
        info['floor'] = soup.select('.room')[0].next.next.next.text
        info['onselltime'] = soup.select('.transaction')[0].select('.label')[0].next.next.next.text
        info['url'] = url
        info['recordtime'] = datetime.datetime.now().isoformat()
        return info
    except:
        print('二手房：获取信息失败，url：'+url)
        return False
