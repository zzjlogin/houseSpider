#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import datetime
import engine
from threading import Thread
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import queue


def fech_allcity_info(fun, cityspell, brief):
    pass

def main():

    cityfile = 'citys.txt'
    city_process = []
    city_list = []
    for brief,spell in engine.get_citypair(cityfile):
        t1 = Thread(target=engine.fech_lianjiainfo_old, args=(spell, brief,))
        # t2 = Thread(target=engine.fech_lianjiainfo_new, args=(spell, brief,))
        t1.start()
        # t2.start()
        print('城市开始爬取数据：\t' + spell)
        city_process.append(t1)
        # city_process.put(t2)
        city_list.append(spell)
        
    while city_process != []:
        check_process = city_process.pop()
        now_city = city_list.pop()
        if check_process.is_alive():
            city_list.append(now_city)
            city_process.append(check_process)
        else:
            print('城市爬取结束：\t'+now_city)
    return True
if __name__ == '__main__':
    print('START: ' + datetime.datetime.now().isoformat())
    start = time.time()
    
    if main():
        # pass
        print(u'用时: ' + str(time.time() - start))
        print('END: ' + datetime.datetime.now().isoformat())
        print('-----succeed!-----' + ' [' + datetime.datetime.now().isoformat() + ']')



