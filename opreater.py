#!/usr/bin/env python
# -*- coding: utf-8 -*-


import lianjia_spider
import writers
import urlhanders
from xpinyin import Pinyin

def wipe_space(s):
    s = str(s)
    s = s.strip()
    s = s.lstrip()
    return s


def get_citypair(filename):
    pinyin = Pinyin()
    
    f = open('citys.txt', encoding='utf-8')
    citys_list = [i.strip().lstrip() for i in f.readlines()]
    f.close()
    citys_pinyin = [pinyin.get_initials(i, splitter='').lower() for i in citys_list]
    return dict(zip(citys_pinyin, [pinyin.get_pinyin(i, splitter='') for i in citys_list])).items()


def fech_lianjiainfo(chinese, pin, num):
    info_detail = 0
    web = u'lianjia'
    tag = False
    for page in urlhanders.generate_allurl(pin, num):
    
        y = lianjia_spider.get_allinfo(page)
        if y == False:
            return True
        for info in y:
            if not tag:
                info_detail = info
                tag = True
            else:
                if info_detail.shape[0] >= 10000:
                    info_detail = info_detail.append(info, ignore_index=True)
                    writers.write_csv(data=info_detail, city=chinese, web=web, neworold=u'ershou')
                    del info_detail
                    tag = False
                else:
                    info_detail = info_detail.append(info, ignore_index=True)
    return writers.write_csv(data=info_detail, city=chinese, web=web)


def fech_newlianjiainfo(chinese, pin, num):
    info_detail = 0
    web = u'lianjia'
    tag = False
    for page in urlhanders.generate_allurl(city=pin, num=num, subdirpre='loupan'):
        informations = lianjia_spider.get_newhous_allinfo(page)
        if informations:
            for info in informations:
                if not tag:
                    info_detail = info
                    tag = True
                else:
                    if info_detail.shape[0] >= 10000:
                        info_detail = info_detail.append(info, ignore_index=True)
                        writers.write_csv(data=info_detail, city=chinese, web=web, neworold=u'xinfang')
                        del info_detail
                        tag = False
                    else:
                        info_detail = info_detail.append(info, ignore_index=True)
        else:
            break
    return writers.write_csv(data=info_detail, city=chinese, web=web, neworold=u'xinfang')
