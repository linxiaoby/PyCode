#!/usr/bin/env python
# encoding:UTF-8

''' Created by wanglin on 2017-9-27'''

import requests as re
import sys
import time

def login(username, password):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0',
    }
    post_data = {'username': username,
                 'password': password,
                 'iprange': 'no',
                 }
    session = re.session()
    session.headers = headers
    response = session.post('https://its.pku.edu.cn/cas/webLogin', data = post_data, verify = False)
    curtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    if response.status_code == 200:
        print curtime + '\treconnet success'
    else:
        print curtime + '\treconnet failed'

if __name__ == '__main__':
    '''
    之前写的检测是否断网的代码有点问题，保险起见，每次都执行网络连接。
    '''
    username = str(sys.argv[1])
    password = str(sys.argv[2])
    login(username, password)
