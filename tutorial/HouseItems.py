#
import scrapy

class HouseItem(scrapy.Item):
    #
    house_type = scrapy.Field()
    #
    house_area = scrapy.Field()
    #
    full_square_meter = scrapy.Field()
    #
    num = scrapy.Field()
    #
    square_meter = scrapy.Field()
    #
    date = scrapy.Field()
    #
    weekday = scrapy.Field()
