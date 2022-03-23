import requests
from bs4 import BeautifulSoup as bs
import json
import random
import pandas
import os 
import logging
from utils import *
from bprint import bprint as print
from urllib.parse import urlencode


class DoubanSpider():
    def __init__(self):
        self.base_url = 'https://movie.douban.com/j/new_search_subjects?'
        self.tags = ['', '电视剧']
        self.genres = ['', '剧情','喜剧','动作','爱情','科幻','动画','悬疑','惊悚','恐怖','犯罪','同性','音乐','歌舞','传记','历史','战争','西部','奇幻','冒险','灾难','武侠','情色']
        self.ua_list = fetch_ua_list()
        self.standard_headers = headers
        self.proxies = proxies
        print (f'Douban Spider initialized', 'green', tag = 'info')
        self.cookies = self._login('kaifan.w3i@gmail.com', 'password111!')

    def _login(self, username, passwd):
        url='https://accounts.douban.com/j/mobile/login/basic'
        data={
            'ck':'',
            'name':username,
            'password':passwd,
            'remember':'false',
            'ticket':''
        }
        data = urlencode(data)
        response = requests.post(url, headers = login_headers, data = data, verify = False)
        cookies = requests.utils.dict_from_cookiejar(response.cookies)
        print ('Logged in', 'green', tag = 'info')
        return cookies
        
        
    def _generate_headers(self):
        _headers = self.standard_headers
        _headers['User-Agent'] = random.choice(self.ua_list)
        return _headers

    def _parse_listing(json_data):
        return

    def _log(self, log_line, log_file = 'douban.log'):
        if not os.path.exists('logs'):
            os.mkdir('logs')
            print(f'Made log folder "logs"', 'blue', tag = 'info')
        else:
            with open(f'logs/{log_file}', 'a') as f:
                f.write(log_line + '\n')

    def _cache_file(self, content, id):
        if not os.path.exists('html_cache'):
            os.mkdir('html_cache')
            print(f'Made cache folder "html_cache"', 'blue', tag = 'info')
        with open(f'html_cache/{id}.html', 'w') as f:
            f.write(content)

    def _make_request(self, url, tag, genre, start):
        params = {'sort': 'U', 'tags': tag, 'genres': genre, 'range': '0,10', 'start': start}
        url = url + urlencode(params)
        response = requests.get(url, proxies = self.proxies, headers = self._generate_headers(), cookies = self.cookies)
        failed = True
        if response.status_code == 200:
            try:
                json_data = response.json()['data']
                print (f'{response.status_code} - {tag} {genre} {start}', 'green', tag = 'info')
                # self._parse_listing(response.json())
                failed = False
            except:
                pass

        if failed:
            # self._log(f'{response.status_code} -- {response.text}')
            self._cache_file(response.text, f'{tag}_{genre}_{start}')
            print (f'{response.status_code} -- {url}', 'red', tag = 'warning')
        
        
    def _request_loop(self, url, tag, genre):
        start = 0
        while start < 200:  
            self._make_request(url, tag, genre, start)
            start += 20
        
    def start_requests(self):
        url = self.base_url
        tags = self.tags
        genres = self.genres
        
        for tag in tags:
            for genre in genres:
                self._request_loop(url, tag, genre)

def main():
    douban = DoubanSpider()
    douban.start_requests()

main()
        
    
