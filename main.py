#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import datetime
import opreater
from threading import Thread

def main():

    user_in_nub = 1
    cityfile = 'citys.txt'
    for p,c in opreater.get_citypair(cityfile):
        t2 = Thread(target=opreater.fech_lianjiainfo, args=(c, p, user_in_nub))
        t1 = Thread(target=opreater.fech_newlianjiainfo, args=(c, p, user_in_nub))
        t1.start()
        t2.start()
        while t1.is_alive() or t2.is_alive():
            if (not t1.is_alive()) and (not t2.is_alive()):
                return True

if __name__ == '__main__':
    print('START: ' + datetime.datetime.now().isoformat())
    start = time.time()
    
    if main():
        pass
    print(u'用时: ' + str(time.time() - start))
    print('END: ' + datetime.datetime.now().isoformat())
    print('-----succeed!-----' + ' [' + datetime.datetime.now().isoformat() + ']')



