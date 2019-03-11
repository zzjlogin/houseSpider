#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import random

def get_proxy_iplist(url='http://www.xicidaili.com/nn/', headers=None,):
    
    
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[1].text + ':' + tds[2].text)
    return ip_list

def generate_allurl(city, num, subdirpre='ershoufang',
                    root='lianjia.com', pagepre = 'pg'):
    url = 'https://{city}.{root}/{subdirpre}/{pagepre}{num}/'
    for url_next in range(1, int(num+1)):
        yield url.format(city=city,
                         root=root,
                         subdirpre=subdirpre,
                         pagepre=pagepre,
                         num=url_next)


