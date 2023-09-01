from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String, Float, Boolean
apartment_data = {
    "monthly_rent": 1000,
    "area": 80,
    "additional_fees": 100,
    "number_of_rooms": "2",
    "deposit": 2000,
    "floor": "3rd",
    "building_type": "Apartment Building",
    "available_from": "2023-09-01",
    "balcony_garden_terrace": "Balcony",
    "remote_service": "Available",
    "finishing_quality": "High",
    "advertiser_type": "Agency",
    "open_to_students": "Yes",
    "furnishing": "Furnished",
    "utilities": "Included",
    "heating": "Central",
    "security": "Guarded Entrance",
    "windows": "Double Glazed",
    "elevator": "Yes",
    "parking_space": "Garage",
    "year_built": "2010",
    "building_material": "Brick",
    "additional_info": "Spacious apartment with great views.",
    "address": "123 Main Street",
    "title": "Modern Apartment with a View",
    "url": "https://example.com/apartment-123",
    "city": "Sample City",
    "county": "Sample County",
    "voivodeship": "Sample Voivodeship",
    "district": "Sample District",
    "neighbourhood": "Sample Neighbourhood",
    "street": "Main Street"
}


Base = declarative_base()
class Apartment(Base):
    __tablename__ = 'apartments'

    # id = mapped_column(Integer, primary_key=True)
    monthly_rent = mapped_column(Integer)
    area = mapped_column(Integer)
    additional_fees = mapped_column(Integer)
    number_of_rooms = mapped_column(String(length=200))
    deposit = mapped_column(Integer)
    floor = mapped_column(String(length=200))
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
    year_built = mapped_column(String(length=200))
    building_material = mapped_column(String(length=200))
    additional_info = mapped_column(String(length=200))
    address = mapped_column(String(length=200))
    title = mapped_column(String(length=200))
    url = mapped_column(String(length=200),primary_key=True)
    city = mapped_column(String(length=200))
    county = mapped_column(String(length=200))
    voivodeship = mapped_column(String(length=200))
    district = mapped_column(String(length=200))
    neighbourhood = mapped_column(String(length=200))
    street = mapped_column(String(length=200))


import sqlalchemy
mysql_url = "mysql+pymysql://root:mysqlpss@localhost:3306/apartments"
import pymysql
engine = sqlalchemy.create_engine(mysql_url,echo=True)
Session = sqlalchemy.orm.sessionmaker()
Session.configure(bind=engine)
session = Session()
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

if not database_exists(engine.url):
    create_database(engine.url)

print(database_exists(engine.url))
Base.metadata.create_all(engine)

newApartament = Apartment(**apartment_data)
session.add(newApartament)
session.add(newApartament)
session.commit()
session.close()

