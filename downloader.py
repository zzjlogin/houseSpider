#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

headers = {
    "User-Agent"     : "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    "Connection"     : "keep-alive",
    "Accept"         : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Referrer Policy": "no - referrer - when - downgrade"}

def downloader(url, headers=headers, proxies=None, timeout=30):
    try:
        url_request = requests.get(url, headers=headers, proxies=proxies, timeout=timeout)
    except:
        print('页面下载失败')
        return False
    if url_request.status_code == 200:
        return url_request.text
    else:
        print('页面状态码不对，获取页面失败')
        return False

