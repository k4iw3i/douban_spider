import json
from w3lib.http import basic_auth_header
import random
import os
from src.secrets_config import *
from urllib.parse import urlencode
import requests
import logging
from src.utils import login_headers

class AltProxiesMiddleware(object):
    def __init__(self):
        self.key = proxy_key
        with open('ua_list.txt', 'r') as f:
            self.ua_list = [x.replace('\n', '') for x in f.readlines()]
        self.cookies = self.login(username, password)

    def login(self, username, password):
        url='https://accounts.douban.com/j/mobile/login/basic'
        data={
            'ck':'',
            'name':username,
            'password':password,
            'remember':'false',
            'ticket':''
        }
        data = urlencode(data)
        response = requests.post(url, headers = login_headers, data = data, verify = False)
        if response.status_code == 200:
            cookies = requests.utils.dict_from_cookiejar(response.cookies)
            logging.info(f'ACCOUNT LOGGED IN \nCookie: {cookies}')
            return cookies
        else:
            logging.error('ACCOUNT LOG IN FAILED -- STATUS CODE: {response.status_code}')
            logging.error(response.text)

    def process_request(self, request, spider):
        request.meta['proxy'] = 'https://zproxy.lum-superproxy.io:22225'
        request.headers['Proxy-Authorization'] = basic_auth_header(
            'lum-customer-c_b6d0914a-zone-static', self.key
        )
        request.headers['User-Agent'] = random.choice(self.ua_list)
        if request.meta['douban']:
            request.headers['Cookie'] = self.cookies
            request.headers['Host'] = 'movie.douban.com'
            request.headers['Referer'] = 'https://movie.douban.com/'
        logging.debug(request.headers)