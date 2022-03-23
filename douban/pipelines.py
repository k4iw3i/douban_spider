from douban.items import *
import os
import pandas as pd
import json
import datetime
import logging

class LocalTestPipeline(object):
    def __init__(self):
        self.item_names = {
            'douban': DoubanItem,
        }
        self.items = {}
        self.item_index = {}
        for item_name in self.item_names.keys():
            self.items[item_name] = []
            self.item_index[item_name] = 0
        self.timestamp = datetime.datetime.today().strftime('%Y-%m-%d')
        if 'output_files' not in os.listdir():
            os.mkdir('output_file')

    def process_item(self, item, spider):
        for item_name in self.item_names.keys():
            item_type = self.item_names[item_name]
            if isinstance(item, item_type):
                self.items[item_name].append(item)
                if len(self.items[item_name])-self.item_index[item_name] > 100:
                    items = self.items[item_name][self.item_index[item_name]:self.item_index[item_name] + 100]
                    self.item_index[item_name] = self.item_index[item_name] + 100
                    self.write_items(items, item_name)
                break
        return item
    
    def write_items(self, items, item_name):
        header = False
        if f'{self.timestamp}_{item_name}.csv' not in os.listdir('output_files'):
            header = True
        item_df = pd.DataFrame(items)
        item_df.to_csv(f'output_files/{self.timestamp}_{item_name}.csv', header = header, index = False, mode = 'a')

    def close_spider(self, spider):
        for item_name in self.item_names.keys():
            items = self.items[item_name][self.item_index[item_name]:]
            self.write_items(items, item_name)
        # items = pd.read_csv(f'output_files/{self.timestamp}_{item_name}.csv')
        # try:
        #     items.to_csv(f's3://kai-freelance-bucket/tieba/results/{self.timestamp}_posts.csv')
        #     logging.info('file uploaded to s3')
        # except Exception as e:
        #     logging.error(f's3 upload error: {e}')
        # return
