from logging import LogRecord
import scrapy
import logging
from scrapy.utils.log import configure_logging 
import re
from ..http import SeleniumRequest
from ..middlewares import SeleniumMiddleware
from ..items import ApartamentItem
import time

# Filtes for redundant log messages
class SeleniumFilter(logging.Filter):
    def filter(self, record: LogRecord) -> bool:
        message = record.getMessage()
        match = re.search(pattern=r"^Remote response: status=200 \| data=",string=message)
        if match:
            return False
        return True


class ApartamentrentspiderSpider(scrapy.Spider):
    details_field_names = [
        'area',
        'additional_fees',
        'number_of_rooms',
        'deposit',
        'floor',
        'building_type',
        'available_from',
        'balcony_garden_terrace',
        'remote_service',
        'finishing_quality',
        'advertiser_type',
        'open_to_students',
        'furnishing',
        'utilities',
        'heating',
        'security',
        'windows',
        'elevator',
        'parking_space',
        'year_built',
        'building_material',
        'additional_info'
    ]

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.page_limit = None
    
        selenium_logger = logging.getLogger("selenium.webdriver.remote.remote_connection")
        selenium_logger.addFilter(SeleniumFilter())
  

    name = "ApartamentRentSpider"
    allowed_domains = ["www.otodom.pl"]

    # You can easily go to website and change filters to scrape the content you want by putting the url with filters applied here.
    start_urls = ["https://www.otodom.pl/pl/wyniki/wynajem/mieszkanie/cala-polska?page=403"]


    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(url=url,
                                  script= "window.scrollTo(0, document.body.scrollHeight);")
        

    def parse(self, response):
        base_ulr = "https://www.otodom.pl"
        apartaments = response.css("a.css-1tiwk2i")


        if self.page_limit == None:
            self.page_limit = int(max(response.xpath("//a[contains(@class,'eo9qioj1 css-5tvc2l edo3iif1')]/text()").getall()))
            logging.info(f"Detected Last Page: {self.page_limit}")
        
            
        for apartament in apartaments:
            time.sleep(1)
            offer_url = apartament.css("a").attrib["href"]
            offer_url = base_ulr + offer_url
            yield scrapy.Request(url=offer_url,callback=self.parse_offer)


        pagenumber = re.search(string=response.url,pattern=r"page=(\d+)")
        pagenumber = int(pagenumber[1])
        logging.info(f"Page number: {pagenumber}")
        if pagenumber < self.page_limit:
            pagenumber += 1
            next_page_url =  re.sub(r"page=(\d+)",f"page={pagenumber}",response.url)
            yield SeleniumRequest(url=next_page_url,callback=self.parse,
                                  script="window.scrollTo(0, document.body.scrollHeight);")

    def parse_offer(self,response):
        apartament = ApartamentItem()
        # apartament = dict()
        apartament["monthly_rent"] = response.css("strong[aria-label='Cena']::text").get()
        description = response.xpath("//div[contains(@class,'e10umaf20')]/div[@aria-label]")
        for x,i in enumerate(description):
            # Optional code that would give polish field names as at the website. Few lines would be have to be commented out and in for it to work.
            # field = i.attrib["aria-label"]
            # field.lower().stip().replace(" ","_")
            # apartament[field] = observation
            observation = i.css("div.css-1wi2w6s::text").get()
            apartament[self.details_field_names[x]] = observation
        apartament["title"] = response.css("h1[data-cy]::text").get()
        apartament["location"] = response.css("a[aria-label='Adres']::text").get()
        apartament["url"] = response.url
        yield apartament
        

