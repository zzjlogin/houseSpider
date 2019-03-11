#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
from parsel import Selector
import pandas as pd
import datetime
import urlhanders
import random

proxies = ''
header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
proxy_ip_list = urlhanders.get_proxy_iplist(headers=header)

def get_random_ip(ip_list=proxy_ip_list):
    ip_list = [ip.strip().lstrip() for ip in ip_list]
    proxy_ip = 'http://' + random.choice(ip_list)
    proxies = {'http': proxy_ip}
    return proxies


def get_allurl(mainpage_url):
    headers = {
        "User-Agent"     : "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        "Connection"     : "keep-alive",
        "Accept"         : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Referrer Policy": "no - referrer - when - downgrade"}
    
    try:
        get_url = requests.get(mainpage_url, headers=headers, proxies=get_random_ip(), timeout=30)
    except:
        return False
    if get_url.status_code == 200:
        url_all = Selector(get_url.text).xpath('//*[@id="content"]/div[1]/ul/li[*]/div[1]/div[1]/a//@href').extract()
        if url_all == []:
            soup = BeautifulSoup(get_url.text, 'lxml')
            try:
                url_n = soup.select('.title')[0].attrs['href']
            except:
                return url_all
            while True:
                for i in range(len(soup.select('.title'))):
                    
                    try:
                        url_n = soup.select('.title')[i].attrs['href']
                        url_all.append(url_n)
                    except:
                        return url_all
                return url_all
        return url_all
    return []


def get_newhouse_allurl(mainpage_url):
    headers = {
        "User-Agent"     : "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        "Connection"     : "keep-alive",
        "Accept"         : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Referrer Policy": "no - referrer - when - downgrade"}
    
    try:
        get_url = requests.get(mainpage_url, headers=headers, proxies=get_random_ip(), timeout=30)
    except:
        return []
    if get_url.status_code == 200:
        url_all = Selector(get_url.text).xpath('/html/body/div[4]/ul[2]/li[*]/div/div[1]/a//@href').extract()
        if url_all == []:
            return []
        url_all = [mainpage_url.split('.com')[0]+'.com'+i for i in url_all]
        return url_all
    return []

def get_info(url_detail):
    
    headers = {
        "User-Agent"     : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        "Connection"     : "keep-alive",
        "Accept"         : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8"}
    if url_detail == []:
        return False
    url_hander = requests.get(url_detail, headers=headers)
    if url_hander.status_code == 200:
        info = {}
        soup = BeautifulSoup(url_hander.text,'lxml')
        info['title'] = soup.select('.title')[0].next.next.text
        info['totalprice'] = soup.select('.total')[0].text
        info['persquaremeterprice'] = soup.select('.unitPriceValue')[0].next
        info['totalarea'] = soup.select('.area')[0].next.next.strip(u'平米')
        #info['villagename_lianjia'] = soup.select('.label')[0].next.next.text
        info['villagename'] = soup.select('.info')[0].text
        info['district'] = soup.select('.info')[1].next.text
        info['housetype'] = soup.select('.base')[0].select('.label')[0].next.next
        info['floor'] = soup.select('.room')[0].next.next.next.text
        info['onselltime'] = soup.select('.transaction')[0].select('.label')[0].next.next.next.text
        info['url'] = url_detail
        info['recordtime'] = datetime.datetime.now().isoformat()
        return info
    return False

def get_newhouse_info(url_detail):
    headers = {
        "User-Agent"     : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        "Connection"     : "keep-alive",
        "Accept"         : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8"}
    if url_detail == []:
        return False
    url_hander = requests.get(url_detail, headers=headers)
    if url_hander.status_code == 200:
        info = {}
        soup = BeautifulSoup(url_hander.text, 'lxml')
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
        info['url'] = url_detail
        info['recordtime'] = datetime.datetime.now().isoformat().strip().lstrip()
        return info
    return False

def get_allinfo(mainpage_i):
    allurl = get_allurl(mainpage_i)
    if allurl == []:
        return False
    for page_i in allurl:
        detail = get_info(page_i)
        if detail == False:
            return False
        info = pd.DataFrame([detail])
        yield info
            
def get_newhous_allinfo(mainpage_i):
    allurl = get_newhouse_allurl(mainpage_i)
    if allurl == []:
        return False
    for page_i in allurl:
        detail = get_newhouse_info(page_i)
        if detail == False:
            return False
        info = pd.DataFrame([detail])
        yield info




