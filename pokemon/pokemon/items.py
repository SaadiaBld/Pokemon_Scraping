# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class PokemonItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    stock = scrapy.Field()
    sku = scrapy.Field()
    categories = scrapy.Field()
    tags = scrapy.Field()
    weight = scrapy.Field()
    dimensions = scrapy.Field()
    
