# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ApartamentItem(scrapy.Item):
    monthly_rent = scrapy.Field()
    area = scrapy.Field()
    additional_fees = scrapy.Field()
    number_of_rooms = scrapy.Field()
    deposit = scrapy.Field()
    floor = scrapy.Field()
    building_type = scrapy.Field()
    available_from = scrapy.Field()
    balcony_garden_terrace = scrapy.Field()
    remote_service = scrapy.Field()
    finishing_quality = scrapy.Field()
    advertiser_type = scrapy.Field()
    open_to_students = scrapy.Field()
    furnishing = scrapy.Field()
    utilities = scrapy.Field()
    heating = scrapy.Field()
    security = scrapy.Field()
    windows = scrapy.Field()
    elevator = scrapy.Field()
    parking_space = scrapy.Field()
    year_built = scrapy.Field()
    building_material = scrapy.Field()
    additional_info =scrapy.Field()
    location = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    city = scrapy.Field()
    county = scrapy.Field()
    voivodeship = scrapy.Field()
    district = scrapy.Field()
    neighbourhood  = scrapy.Field()
    street = scrapy.Field()


