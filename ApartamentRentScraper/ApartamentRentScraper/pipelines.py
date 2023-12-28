# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re
import sqlalchemy
import logging



from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.exc import IntegrityError


class ApartamentScraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # Removing characters from numerical fields      
        numerical  = ["monthly_rent","deposit","additional_fees","area"]
        for field in numerical:
            if adapter[field]:
                adapter[field] = int(re.sub(r"[^\d.,]+|[.,].+","",adapter[field].replace(" ","")))
        
        # The adress comes in two patterns we can use it to categorize it's components.
        adreses = adapter["location"].split(", ")
        adreses.reverse()
        adapter["voivodeship"] = adreses[0]
        if adreses[1].istitle():
            adapter["city"] = adreses[1]
            adapter["county"] = adreses[1]
            for position,adres in enumerate(adreses[2:],start=2):
                if adres.istitle():
                    if position == 2:
                        if not re.search(r"\d",adres):
                            adapter["district"] = adres
                    elif position == 3:
                        adapter["neighbourhood"] = adres
                else:
                    adapter["street"] = adres

        else:
            adapter["county"] = adreses[1]
            adapter["city"] = adreses[2]
            for position,adres in enumerate(adreses[3:],start=3):
                if adres.istitle():
                    if position == 3:
                        adapter["district"] = adres
                    elif position == 4:
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


from .schemas import Base,ApartamentCassandra,ApartamentMySQL

class MySQLPipeline:
    """
    Pipeline for storing scraped apartment items in a MySQL database.
    
    This pipeline allows for batch inserts, and handles integrity errors by attempting individual inserts
    for items that failed during batch insert.
    """
    
    def __init__(self, mysql_url):
        self.mysql_url = mysql_url
        self.batch_size = 0
        self.staged_items = []
    @classmethod
    
    def from_crawler(cls, crawler):
        return cls(
            mysql_url=crawler.settings.get("MYSQL_URL"),
        )

    def open_spider(self, spider):
        self.THRESHOLD = spider.settings.get('BATCH_THRESHOLD',100)
        
        self.engine = sqlalchemy.create_engine(self.mysql_url,echo=True)
        Session = sqlalchemy.orm.sessionmaker()
        Session.configure(bind=self.engine)
        if not database_exists(self.engine.url):
            create_database(self.engine.url)

        Base.metadata.create_all(self.engine)
        self.session = Session()

    def close_spider(self, spider):
        if self.batch_size > 0:
            self.mysql_commit()
        self.session.close()

    def process_item(self,item,spider):
        apartament = ItemAdapter(item).asdict()
        newApartament = ApartamentMySQL(**apartament)
        self.session.add(newApartament)
        self.staged_items.append(newApartament)  # Add the item to the list in case of failed batch commit. 
        self.batch_size += 1

        if self.batch_size >= self.THRESHOLD:
            self.mysql_commit()
        return item
    
    
    def mysql_commit(self):
        try:
            self.session.commit()
            self.batch_size = 0
            self.staged_items.clear()  # Clear the list since items were successfully committed
            logging.info("Batch commit sucessful")
        except IntegrityError as e:
            self.session.rollback()
            logging.warning(f"Batch insert failed: {repr(e)}. Reverting to individual inserts.")
            for singleApartament in self.staged_items:
                try:
                    self.session.add(singleApartament)
                    self.session.commit()
                except IntegrityError as sub_e:
                    self.session.rollback()
                    if "Duplicate entry" in repr(sub_e):
                        logging.info("Failed to insert item. Reason: Duplicate Entry.")
                    else:
                        logging.error(f"Failed to insert item: {repr(sub_e)}")
            self.staged_items.clear()  # Clear the list after processing
            self.batch_size = 0
                

from cassandra.cluster import Cluster
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from itemadapter import ItemAdapter
from cassandra import DriverException

class CassandraPipeline:
    """
    Pipeline for storing scraped apartment items in a Cassandra database.
    
    This pipeline connects to a Cassandra cluster, ensures the required table exists, and then stores the scraped items.
    """

    def __init__(self, host, port, keyspace):
        """
        Initializes the Cassandra pipeline.
        
        Args:
            host (str): The host address of the Cassandra cluster.
            port (int): The port number for connecting to the Cassandra cluster.
            keyspace (str): The keyspace to use in the Cassandra cluster.
        """
        self.host = host
        self.port = port
        self.keyspace = keyspace

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get("CASSANDRA_HOST"),
            port=crawler.settings.get("CASSANDRA_PORT"),
            keyspace=crawler.settings.get("CASSANDRA_KEYSPACE")
        )

    def open_spider(self, spider):
        # Connect to the Cassandra cluster
        self.cluster = Cluster([self.host], port=self.port)
        self.session = self.cluster.connect(self.keyspace)
        connection.set_session(self.session)
        sync_table(ApartamentCassandra)  # Ensure the table exists

    def process_item(self, item, spider):
        item_dict = ItemAdapter(item).asdict()
        ApartamentCassandra.create(**item_dict)
        return item

    def close_spider(self, spider):
        self.cluster.shutdown()
    
