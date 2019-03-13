#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import datetime

def get_proxy_iplist(pagedetail_txt):
    
    soup = BeautifulSoup(pagedetail_txt, 'lxml')
    try:
        ips = soup.find_all('tr')
    except:
        return []
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        try:
            tds = ip_info.find_all('td')
        except:
            return []
        ip_list.append(tds[1].text + ':' + tds[2].text)
    return ip_list


def get_info_oldhouse(page_txt, url):
    print('获取二手房item信息：' + url)
    info = {}
    try:
        soup = BeautifulSoup(page_txt, 'lxml')
        info['title'] = soup.select('.title')[0].next.next.text
        info['totalprice'] = soup.select('.total')[0].text
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
        print('二手房：获取信息失败')
        return False


def get_info_newhouse(page_txt, url):
    print('获取新房item信息：'+url)
    info = {}
    try:
        soup = BeautifulSoup(page_txt, 'lxml')
        info['saleoffice'] = soup.select('.label-val')[1].text.strip().lstrip()
        info['developor'] = soup.select('.label-val')[2].text.strip().lstrip()
        info['persquaremeterprice'] = soup.select('.junjia')[0].text.strip().lstrip()
        info['onselltime'] = soup.select('.label-val')[4].text.strip().lstrip()
        # info['villagename_lianjia'] = soup.select('.label')[0].next.next.text
        info['villagename'] = soup.select('.DATA-PROJECT-NAME')[0].text.strip().lstrip()
        info['projectadress'] = soup.select('.label-val')[0].text.strip().lstrip()
        info['housetype'] = soup.select('.label-val')[5].text.strip().lstrip()
        info['floor'] = soup.select('.label-val')[16].text.strip().lstrip()
        info['deliverytime'] = soup.select('.label-val')[6].text.strip().lstrip()
        info['url'] = url
        info['recordtime'] = datetime.datetime.now().isoformat().strip().lstrip()
        return info
    except:
        print('新房：获取信息失败（items文件）')
        return False



