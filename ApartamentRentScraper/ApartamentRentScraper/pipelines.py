# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re
import sqlalchemy
import logging


from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String, Float, Boolean
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.exc import IntegrityError


class ApartamentScraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        # Remowing all non-digit characters and converting to integers
        
        numerical  = ["monthly_rent","deposit","additional_fees","area"]
        for field in numerical:
            if adapter[field]:
                adapter[field] = int(re.sub(r"\D+","",adapter[field]))
        
        adreses = adapter["location"].split(", ")
        adreses.reverse()
        adapter["voivodeship"] = adreses[0]
        if adreses[1].istitle():
            adapter["city"] = adreses[1]
            adapter["county"] = adreses[1]
            for i,adres in enumerate(adreses[2:],start=2):
                if adres.istitle():
                    if i == 2:
                        adapter["district"] = adres
                    elif i == 3:
                        adapter["neighbourhood"] = adres
                else:
                    adapter["street"] = adres

        else:
            adapter["county"] = adreses[1]
            adapter["city"] = adreses[2]
            for i,adres in enumerate(adreses[3:],start=3):
                if adres.istitle():
                    if i == 3:
                        adapter["district"] = adres
                    elif i == 4:
                        adapter["neighbourhood"] = adres
                else:
                    adapter["street"] = adres

        return item
    
    def __init__(self, mysql_url):
        self.mysql_url = mysql_url

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mysql_url=crawler.settings.get("MYSQL_URL"),
        )



Base = declarative_base()
class Apartament(Base):
    __tablename__ = 'apartaments'
    # id = mapped_column(Integer, primary_key=True)
    monthly_rent = mapped_column(Integer)
    area = mapped_column(Integer)
    additional_fees = mapped_column(Integer)
    number_of_rooms = mapped_column(String(length=10))
    deposit = mapped_column(Integer)
    floor = mapped_column(String(length=20))
    building_type = mapped_column(String(length=200))
    available_from = mapped_column(String(length=200))
    balcony_garden_terrace = mapped_column(String(length=200))
    remote_service = mapped_column(String(length=200))
    finishing_quality = mapped_column(String(length=200))
    advertiser_type = mapped_column(String(length=200))
    open_to_students = mapped_column(String(length=200))
    furnishing = mapped_column(String(length=200))
    utilities = mapped_column(String(length=200))
    heating = mapped_column(String(length=200))
    security = mapped_column(String(length=200))
    windows = mapped_column(String(length=200))
    elevator = mapped_column(String(length=200))
    parking_space = mapped_column(String(length=200))
    year_built = mapped_column(String(length=20))
    building_material = mapped_column(String(length=200))
    additional_info = mapped_column(String(length=200))
    location = mapped_column(String(length=200))
    title = mapped_column(String(length=200))
    url = mapped_column(String(length=500),primary_key=True)
    city = mapped_column(String(length=200))
    county = mapped_column(String(length=200))
    voivodeship = mapped_column(String(length=200))
    district = mapped_column(String(length=200))
    neighbourhood = mapped_column(String(length=200))
    street = mapped_column(String(length=200))


class MySQLPipeline:
    def __init__(self, mysql_url):
        self.mysql_url = mysql_url 
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mysql_url=crawler.settings.get("MYSQL_URL"),
        )

    def open_spider(self, spider):
        self.engine = sqlalchemy.create_engine(self.mysql_url,echo=True)
        Session = sqlalchemy.orm.sessionmaker()
        Session.configure(bind=self.engine)
        if not database_exists(self.engine.url):
            create_database(self.engine.url)

        Base.metadata.create_all(self.engine)
        self.session = Session()

    def close_spider(self, spider):
        self.session.close()

    def process_item(self,item,spider):
        apartament = ItemAdapter(item).asdict()
        # logging.debug(f"{f'{tuple(zip(apartament.items(),[type(x) for x in list(apartament.values())]))}'}")
        newApartament = Apartament(**apartament)

        try:
            self.session.add(newApartament)
            self.session.commit()
        except IntegrityError as e:
            self.session.rollback()
            error_repr = repr(e)
            if "Duplicate entry" in error_repr:
                logging.info("Duplicate entry detected.")
            else:
                logging.error(error_repr)


        return item
    
