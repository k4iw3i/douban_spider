from src.spider_config import concurrent_requests, download_delay

BOT_NAME = 'douban'

SPIDER_MODULES = ['douban.spiders']
NEWSPIDER_MODULE = 'douban.spiders'

ROBOTSTXT_OBEY = False
LOG_LEVEL = 'INFO'

CONCURRENT_REQUESTS = concurrent_requests
DOWNLOAD_DELAY = download_delay

RETRY_HTTP_CODES = [403, 302]