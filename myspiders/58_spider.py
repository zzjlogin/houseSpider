#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from parsel import Selector
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_houseurls_old(mainpage_txt):
    # print('执行：get_houseurls_old')
    try:
        url_all = Selector(mainpage_txt).xpath('/html/body/div[5]/div[5]/div[1]/ul/li[*]/div[2]/h2/a/@href').extract()
    except:
        return []
    #print('二手房urls：'+str(url_all))
    return url_all

def get_houseurls_new(mainpage_txt):
    # print('执行：get_houseurls_new')
    try:
        url_all = Selector(mainpage_txt).xpath('/html/body/div[4]/ul[2]/li[*]/div/div[1]/a//@href').extract()
        soup = BeautifulSoup(mainpage_txt, 'lxml')
        regionlink = soup.select('.new-link-list')[1].next.next.attrs.get('href')
        if 'https://' in regionlink:
            url_all = [regionlink.strip('/') + i for i in url_all]
        else:
            url_all = ['https://'+regionlink.strip('/') + i for i in url_all]
        # print(url_all)
        return url_all
    except:
        return []

def get_mainurls_old(mainpage_txt):
    # print('执行：get_mainurls_old')
    soup = BeautifulSoup(mainpage_txt, 'lxml')
    try:
        end_list = Selector(mainpage_txt).xpath('/html/body/div[5]/div[5]/div[1]/div[2]/a//@href').extract()[-2].strip('/').split('pn')
        end = int(end_list[-1])
    except:
        print('获取所有网页数失败: 43行')
        return False
    try:
        regionlink = soup.select('.on')[0].next.next.attrs['href']
    except:
        print('获取所有网页数失败：49行')
        return False
    regionlink = regionlink + 'pn'
    # print('totalPage'+str(end))
    for i in range(2, end+1):
        # print('处理主页url地址：'+regionlink + str(i))
        yield regionlink + str(i)

def get_mainurls_new(mainpage_txt):
    soup = BeautifulSoup(mainpage_txt, 'lxml')
    try:
        num_url = soup.select('.page-box')[0].attrs
    except:
        print('获取所有网页数失败：63行')
        return False
    try:
        regionlink = soup.select('.new-link-list')[1].next.next.attrs.get('href')
    except:
        print('获取所有网页数失败：68行')
        return False
    if 'https:' in regionlink:
        regionlink = regionlink + 'loupan/pg'
    else:
        regionlink = 'https:' + regionlink + 'loupan/pg'
    start = int(num_url.get('data-current'))
    end = int(num_url.get('data-total-count'))
    for i in range(start+1, end+1):
        # print(regionlink+str(i))
        yield regionlink + str(i)
