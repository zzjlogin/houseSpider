#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import items
import pandas as pd



def write_csv(data, city, web=u'lianjia', neworold=u'ershou' ,mode='a' ,encoding='utf_8_sig'):
    sep = os.path.sep
    filedir = 'data' + sep + web + sep + city + sep + neworold
    order = list(data.columns)
    order.sort()
    data = data[order]
    if not os.path.exists(filedir):
        try:
            os.makedirs(filedir)
        except:
            return False
    filename = filedir + sep + time.strftime("%Y%m%d") + '.csv'
    if os.path.lexists(filename) and os.path.isfile(filename):
        data.to_csv(filename, mode=mode, encoding=encoding, index=0, header=0)
    else:
        data.to_csv(filename, mode=mode, encoding=encoding, index=0)
    # info_detail = pd.DataFrame(columns=order)
    print(u'写入成功: '+filename)
    return True



