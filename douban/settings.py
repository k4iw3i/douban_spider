BOT_NAME = 'douban'

SPIDER_MODULES = ['douban.spiders']
NEWSPIDER_MODULE = 'douban.spiders'

ROBOTSTXT_OBEY = False
LOG_LEVEL = 'INFO'

CONCURRENT_REQUESTS = 12
DOWNLOAD_DELAY = 0

RETRY_HTTP_CODES = [403, 302]