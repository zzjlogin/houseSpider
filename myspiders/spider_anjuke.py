#!/usr/bin/env python
# -*- coding: utf-8 -*-



from bs4 import BeautifulSoup
from parsel import Selector
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_mainurls_old(mainpage_txt):
    # print('执行：get_mainurls_old')
    main_urls = Selector(d).xpath('//*[@id="content"]/div[4]/div[7]/a//@href').extract
    return main_urls

def get_houseurls_old(mainpage_txt):
    
    try:
        soup = BeautifulSoup(mainpage_txt, 'lxml')
    except:
        return []
    partpage = soup.select('.houseListTitle')
    house_urls = []
    for i in partpage:
        url = i.attrs.get('href')
        house_urls.append(url)
    return house_urls

