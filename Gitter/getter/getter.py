#!/usr/bin/env python

import os

import requests

# https://gitter.im/alerta/chat/archives/2015/09/29

from datetime import timedelta, date

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

#start_date = date(2015, 9, 29)
#end_date = date(2021, 6, 2)
start_date = date(2021, 6, 2)
end_date = date(2021, 10, 23)
for single_date in daterange(start_date, end_date):

    filename = 'gitter-alerta-{}.txt.html'.format(single_date.strftime("%Y%m%d"))
    print(filename)
    if os.path.exists(filename):
        continue

    url = 'https://gitter.im/alerta/chat/archives/{}'.format(single_date.strftime("%Y/%m/%d"))
    r = requests.get(url)

    f = open(filename, 'a')
    f.write(r.text)
    f.close()

    import time
    time.sleep(5)

