#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import datetime
import engine
from threading import Thread

def fech_allcity_info(fun, cityspell, brief):
    pass


def main():

    cityfile = 'citys.txt'
    citythread_pre = []
    citythread_processing = []
    for brief,spell in engine.get_citypair(cityfile):
        citythread_pre.append(Thread(target=engine.fech_lianjiainfo_old, args=(spell, brief,)))
        citythread_pre.append(Thread(target=engine.fech_lianjiainfo_new, args=(spell, brief,)))
        for i in range(2):
            tep = citythread_pre.pop()
            tep.start()
            citythread_processing.append(tep)
        print('城市开始爬取数据：\t'+spell)
    while citythread_processing != []:
        for i in range(len(citythread_processing)):
            nowtheading = citythread_processing.pop()
            if nowtheading.is_alive():
                citythread_processing.append(nowtheading)
            else:
                pass
    return True
if __name__ == '__main__':
    print('START: ' + datetime.datetime.now().isoformat())
    start = time.time()
    
    if main():
        # pass
        print(u'用时: ' + str(time.time() - start))
        print('END: ' + datetime.datetime.now().isoformat())
        print('-----succeed!-----' + ' [' + datetime.datetime.now().isoformat() + ']')



