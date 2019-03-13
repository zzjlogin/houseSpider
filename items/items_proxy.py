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

