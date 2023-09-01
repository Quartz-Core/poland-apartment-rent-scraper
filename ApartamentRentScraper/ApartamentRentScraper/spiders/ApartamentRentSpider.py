import scrapy
import logging
from scrapy.utils.log import configure_logging 
import re
from ..http import SeleniumRequest
from ..middlewares import SeleniumMiddleware
from ..items import ApartamentItem


class ApartamentrentspiderSpider(scrapy.Spider):
    configure_logging(install_root_handler=False)
    logging.basicConfig(
    filename='log.txt',
    format='%(levelname)s: %(message)s',
    level=logging.INFO
    )

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
  

    name = "ApartamentRentSpider"
    allowed_domains = ["www.otodom.pl"]

    # You can easily go to website and change filters to scrape the content you want by putting the url with filters applied here.
    start_urls = ["https://www.otodom.pl/pl/wyniki/wynajem/mieszkanie/cala-polska?page=1"]


    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(url=url,
                                  script= "window.scrollTo(0, document.body.scrollHeight);")
        

    def parse(self, response):
        base_ulr = "https://www.otodom.pl"
        apartaments = response.css("a.css-1tiwk2i")

        if self.page_limit == None:
            self.page_limit = max(response.xpath("//a[contains(@class,'eo9qioj1 css-5tvc2l edo3iif1')]/text()").getall())

        for apartament in apartaments:
            offer_url = apartament.css("a").attrib["href"]
            offer_url = base_ulr + offer_url
            yield scrapy.Request(url=offer_url,callback=self.parse_offer)


        pagenumber = re.search(string=response.url,pattern=r"page=(\d+)")
        pagenumber = int(pagenumber[1])
        if pagenumber < self.page_limit:
            pagenumber += 1
            next_page_url = f"https://www.otodom.pl/pl/wyniki/wynajem/kawalerka/cala-polska?page={pagenumber}&by=LATEST&direction=ASC"
            yield SeleniumRequest(url=next_page_url,callback=self.parse,
                                  script="window.scrollTo(0, document.body.scrollHeight);")

    def parse_offer(self,response):
        apartament = ApartamentItem()
        # Replacing items with dicts would give more dynamic web scraper sturcture. Currently not avalible. 
        # apartament = dict()
        apartament["monthly_rent"] = response.css("strong[aria-label='Cena']::text").get()
        description = response.xpath("//div[contains(@class,'e10umaf20')]/div[@aria-label]")
        for x,i in enumerate(description):
            # field = i.attrib["aria-label"]
            # field.lower().stip().replace(" ","_")
            # apartament[field] = observation
            observation = i.css("div.css-1wi2w6s::text").get()
            apartament[self.details_field_names[x]] = observation
        apartament["title"] = response.css("h1[data-cy]::text").get()
        apartament["location"] = response.css("a[aria-label='Adres']::text").get()
        apartament["url"] = response.url
        yield apartament
        

