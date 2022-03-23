from email import header
import logging
import json
from douban.items import *
import scrapy
import os
import datetime
import pandas as pd
import fuckit
from src.utils import *
from bs4 import BeautifulSoup as bs
import sys
import csv
import time
from scrapy.exceptions import CloseSpider
import re
from urllib.parse import urlencode
from src.spider_config import *
csv.field_size_limit(sys.maxsize)


today = datetime.datetime.today().strftime('%Y-%m-%d ')


class TiebaSpider(scrapy.Spider):
    custom_settings = {
        'ITEM_PIPELINES': {
            'douban.pipelines.LocalTestPipeline': 300,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'douban.middlewares.AltProxiesMiddleware': 720,
        },
    }
    name = 'douban_spider'

    def __init__(self, **kwargs):
        self.base_url = 'https://movie.douban.com/j/new_search_subjects?'
        self.tags = tags
        self.genres = genres
        self.sort = sort
        self.huoxing_max_page = huoxing_max_page
        self.douban_max_item_per_search = douban_max_item_per_search
        if self.huoxing_max_page > 0:
            logging.info('HUOXING ENABLED')
        else:
            logging.info('HUOXING DISABLED')

    def start_requests(self):
        for tag in self.tags:
            for genre in self.genres:
                for sort in self.sort:
                    start = 0
                    params = {'sort': sort, 'tags': tag, 'genres': genre, 'range': '0,10', 'start': start}
                    url = self.base_url + urlencode(params)
                    yield scrapy.Request(url, headers = headers, callback = self.parse_listing, meta = {'start': start, 'params': params, 'douban': True})
                
        if self.huoxing_max_page > 0:
            for page_num in range(1, self.huoxing_max_page + 1):
                url = f'https://huo720.com/calendar/thismonth/{page_num}'
                yield scrapy.Request(url, headers = headers, callback = self.parse_mars_listing, meta = {'douban': False})
        
    def parse_mars_listing(self, response):
        soup = bs(response.text, 'html.parser')
        movie_urls = ['https://huo720.com' + x.find('a', {'f16 link-dark'})['href'] for x in soup.find_all('div', {'class': 'row g-0'})]
        for movie_url in movie_urls:
            yield scrapy.Request(movie_url, callback = self.parse_mars_detail, meta = {'douban': False})

    def parse_mars_detail(self, response):
        soup = bs(response.text, 'html.parser')
        douban_url = soup.find('div', {'class': 'rounded-3 bg-douban d-inline p-1'}).find_next('a')['href']
        if 'null' not in douban_url:
            yield scrapy.Request(douban_url, callback = self.parse_detail, meta = {'douban': True})
        else:
            logging.debug(f'DOUBAN LINK NOT FOUND: {response.request.url}')


    def parse_listing(self, response):
        start = response.meta['start']
        try:
            json_data = json.loads(response.text)['data']
        except:
            logging.error(response.text)
            return

        for record in json_data:
            media_url = record['url']
            yield scrapy.Request(media_url, headers = headers, callback = self.parse_detail, meta = {'dont_redirect': True, 'douban': True})

        start += 20
        if start < self.douban_max_item_per_search:
            params = response.meta['params']
            params['start'] = start
            url = self.base_url + urlencode(params)
            yield scrapy.Request(url, callback = self.parse_listing, meta = {'start': start, 'params': params, 'douban': True})
        
    def parse_detail(self, response):
        soup = bs(response.text, 'html.parser')
        # media = response.meta['item']
        media = DoubanItem()
        json_data = json.loads(soup.find('script', {'type': 'application/ld+json'}).text, strict = False)
        media['url'] = response.request.url
        media['douban_id'] = re.sub("[^0-9]", "", response.request.url)
        media['title'] = json_data['name']
        media['rating'] = json_data['aggregateRating']['ratingValue']
        media['rating_number'] = json_data['aggregateRating']['ratingCount']
        media['casts'] = [x['name'] for x in json_data['actor']] if len(json_data['actor']) > 0 else None
        media['cover_image'] = json_data['image']
        media['directors'] = [x['name'] for x in json_data['director']] if len(json_data['director']) > 0 else None
        media['writers'] = [x['name'] for x in json_data['author']] if len(json_data['author']) > 0 else None
        media['genres'] = json_data['genre']
        media['release_date'] = json_data['datePublished']
        media['duration'] = json_data['duration']
        media['description'] = json_data['description']
        media['media_type'] = json_data['@type']

        with fuckit:
            comments_div = soup.find('div', {'id': 'comments-section'})
            media['comment_number'] = re.sub("[^0-9]", "", [x for x in comments_div.find_all('a') if '全部' in x.text][0].text)
        with fuckit:
            reviews_div = soup.find('section', {'id': 'reviews-wrapper'})
            media['review_number'] = re.sub("[^0-9]", "", [x for x in reviews_div.find_all('a') if '全部' in x.text][0].text)
        other_interest_div = soup.find('div', {'class': 'subject-others-interests-ft'})
        with fuckit: 
            media['watching_number'] = re.sub("[^0-9]", "", [x for x in other_interest_div.find_all('a') if '在看' in x.text][0].text)
        with fuckit:
            media['watched_number'] = re.sub("[^0-9]", "", [x for x in other_interest_div.find_all('a') if '看过' in x.text][0].text)
        with fuckit:
            media['want_to_watch_number'] = re.sub("[^0-9]", "", [x for x in other_interest_div.find_all('a') if '想看' in x.text][0].text)
        # logging.info(media)
        yield media
