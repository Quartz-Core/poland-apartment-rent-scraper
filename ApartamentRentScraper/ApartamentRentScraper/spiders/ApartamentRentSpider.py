from logging import LogRecord
import scrapy
import logging
from scrapy.utils.log import configure_logging 
import re
from ..items import ApartamentItem
import time

from scrapy_seleniumbase import SeleniumBaseRequest


# Filter for redundant log messages
class SeleniumFilter(logging.Filter):
    def filter(self, record: LogRecord) -> bool:
        message = record.getMessage()
        match = re.search(pattern=r"^Remote response: status=200 \| data=",string=message)
        if match:
            return False
        return True


class ApartamentrentspiderSpider(scrapy.Spider):
    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.page_limit = None
    
        selenium_logger = logging.getLogger("selenium.webdriver.remote.remote_connection")
        selenium_logger.addFilter(SeleniumFilter())
        


  

    name = "ApartamentRentSpider"
    allowed_domains = ["www.otodom.pl"]

    # You can easily go to website and change filters to scrape the content you want by putting the url with filters applied here.
    start_urls = ["https://www.otodom.pl/pl/wyniki/wynajem/mieszkanie/cala-polska?limit=72&page=1"]
    


    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumBaseRequest(url=url,
                                  script= "window.scrollTo(0, document.body.scrollHeight);",
                                  driver_methods=['''.find_element(value='//*[@id="onetrust-accept-btn-handler"]',by="xpath").click()'''])
        

    def parse(self, response):
        base_ulr = "https://www.otodom.pl"
        apartaments = response.css('a[data-cy="listing-item-link"]')
        
        if self.page_limit == None:
            self.page_limit = int(max(response.css("li.css-1tospdx::text").getall()))
            logging.info(f"Detected Last Page: {self.page_limit}")
        
        for apartament in apartaments:
            offer_url = apartament.css("a").attrib["href"]
            offer_url = base_ulr + offer_url

            yield scrapy.Request(url=offer_url,callback=self.parse_offer)


        pagenumber = re.search(string=response.url,pattern=r"page=(\d+)")
        pagenumber = int(pagenumber[1])
        logging.info(f"Page number: {pagenumber}")
        if pagenumber < self.page_limit:
            pagenumber += 1
            next_page_url =  re.sub(r"page=(\d+)",f"page={pagenumber}",response.url)
            yield SeleniumBaseRequest(url=next_page_url,callback=self.parse,
                                  script="window.scrollTo(0, document.body.scrollHeight);")

    def parse_offer(self,response):
        apartament = ApartamentItem()
        
        apartament["monthly_rent"] = response.css("strong[aria-label='Cena']::text").get()
        # description_details = response.xpath("//div[contains(@class,'e10umaf20')]/div[@aria-label]")
        apartament['area'] = response.css('div[aria-label="Powierzchnia"] div[data-testid]::text').get()
        apartament['additional_fees'] = response.css('div[aria-label="Czynsz"] div[data-testid]::text').get()
        apartament['number_of_rooms'] = response.css('div[aria-label="Liczba pokoi"] div[data-testid]::text').get()
        apartament['deposit'] = response.css('div[aria-label="Kaucja"] div[data-testid]::text').get()
        apartament['floor'] = response.css('div[aria-label="Piętro"] div[data-testid]::text').get()
        apartament['building_type'] = response.css('div[aria-label="Rodzaj zabudowy"] div[data-testid]::text').get()
        apartament['available_from'] = response.css('div[aria-label="Dostępne od"] div[data-testid]::text').get()
        apartament['balcony_garden_terrace'] = response.css('div[aria-label="Balkon / ogród / taras"] div[data-testid]::text').get()
        apartament['remote_service'] = response.css('div[aria-label="Obsługa zdalna"] div[data-testid]::text').get()
        apartament['finishing_quality'] = response.css('div[aria-label="Stan wykończenia"] div[data-testid]::text').get()
        apartament['advertiser_type'] = response.css('div[aria-label="Typ ogłoszeniodawcy"] div[data-testid]::text').get()
        apartament['open_to_students'] = response.css('div[aria-label="Wynajmę również studentom"] div[data-testid]::text').get()
        apartament['furnishing'] = response.css('div[aria-label="Wyposażenie"] div[data-testid]::text').get()
        apartament['utilities'] = response.css('div[aria-label="Media"] div[data-testid]::text').get()
        apartament['heating'] = response.css('div[aria-label="Ogrzewanie"] div[data-testid]::text').get()
        apartament['security'] = response.css('div[aria-label="Zabezpieczenia"] div[data-testid]::text').get()
        apartament['windows'] = response.css('div[aria-label="Okna"] div[data-testid]::text').get()
        apartament['elevator'] = response.css('div[aria-label="Winda"] div[data-testid]::text').get()
        apartament['parking_space'] = response.css('div[aria-label="Miejsce parkingowe"] div[data-testid]::text').get()
        apartament['year_built'] = response.css('div[aria-label="Rok budowy"] div[data-testid]::text').get()
        apartament['building_material'] = response.css('div[aria-label="Materiał budynku"] div[data-testid]::text').get()
        apartament['additional_info'] = response.css('div[aria-label="Informacje dodatkowe"] div[data-testid]::text').get()
 
        apartament["title"] = response.css("h1[data-cy]::text").get()
        apartament["location"] = response.css("a[aria-label='Adres']::text").get()
        apartament["url"] = response.url
        
        yield apartament
        
    






















