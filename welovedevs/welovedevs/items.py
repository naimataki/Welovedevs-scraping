# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class JobItem(scrapy.Item):
    title = scrapy.Field()
    experience = scrapy.Field()
    contract_type = scrapy.Field()
    salary_range = scrapy.Field()
    job_type = scrapy.Field()

    pass

