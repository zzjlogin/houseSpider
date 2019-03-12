#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from parsel import Selector

def get_houseurls_old(mainpage_txt):
    
    try:
        url_all = Selector(mainpage_txt).xpath('//*[@id="content"]/div[1]/ul/li[*]/div[1]/div[1]/a//@href').extract()
    except:
        return []
    if url_all == []:
        soup = BeautifulSoup(mainpage_txt, 'lxml')
        try:
            partpage = soup.select('.title')
        except:
            return url_all
        while True:
            for i in range(len(partpage)):
                url_n = partpage[i].attrs
                if 'href' in url_n:
                    url_all.append(url_n.get('href'))
                else:
                    return url_all
            return url_all
    return url_all

def get_houseurls_new(mainpage_txt):
    try:
        url_all = Selector(mainpage_txt).xpath('/html/body/div[4]/ul[2]/li[*]/div/div[1]/a//@href').extract()
        soup = BeautifulSoup(mainpage_txt, 'lxml')
        regionlink = soup.select('.new-link-list')[1].next.next.attrs.get('href')
        url_all = ['https://'+regionlink.strip('/') + i for i in url_all]
        return url_all
    except:
        return []

def get_mainurls_old(mainpage_txt):

    soup = BeautifulSoup(mainpage_txt, 'lxml')
    try:
        num_url = eval(soup.select('.page-box')[0].next.attrs['page-data'])
    except:
        print('获取所有网页数失败')
        return False
    try:
        regionlink = soup.select('.selected')[0].next.attrs.get('href')
    except:
        print('获取所有网页数失败')
        return False
    regionlink = regionlink + 'pg'
    start = num_url.get('totalPage')
    end = num_url.get('curPage')
    for i in range(start, end+1):
        yield regionlink + str(i)

def get_mainurls_new(mainpage_txt):

    soup = BeautifulSoup(mainpage_txt, 'lxml')
    try:
        num_url = eval(soup.select('.page-box')[0].attrs)
    except:
        print('获取所有网页数失败')
        return False
    try:
        regionlink = soup.select('.new-link-list')[1].next.next.attrs.get('href')
    except:
        print('获取所有网页数失败')
        return False
    regionlink = 'https:' + regionlink + 'loupan/pg'
    start = int(num_url.get('data-current'))
    end = int(num_url.get('data-total-count'))
    for i in range(start, end+1):
        yield regionlink + str(i)