import scrapy


class DoubanItem(scrapy.Item):
    title = scrapy.Field() #parse_listing
    url = scrapy.Field() #parse_listing
    rating = scrapy.Field() #parse_listing
    rating_number = scrapy.Field()
    directors = scrapy.Field() #parse_listing
    writers = scrapy.Field()
    casts = scrapy.Field() #parse_listing
    cover_image = scrapy.Field() #parse_listing
    douban_id = scrapy.Field() #parse_listing
    comment_number = scrapy.Field()
    review_number = scrapy.Field()
    watching_number = scrapy.Field()
    watched_number = scrapy.Field()
    want_to_watch_number = scrapy.Field()
    genres = scrapy.Field()
    release_date = scrapy.Field()
    description = scrapy.Field()
    duration = scrapy.Field()
    media_type = scrapy.Field()
    pass
