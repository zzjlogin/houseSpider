#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import datetime
import engine
from threading import Thread


def main():

    cityfile = 'citys.txt'
    for brief,spell in engine.get_citypair(cityfile):
        t2 = Thread(target=engine.fech_lianjiainfo, args=(spell, brief,))
        t1 = Thread(target=engine.fech_lianjiainfo_new, args=(spell, brief,))
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



