# Some schemas for pipelines.py. You should probably use your own.



# from sqlalchemy.orm import declarative_base
# from sqlalchemy.orm import mapped_column
# from sqlalchemy import Integer, String, Float, Boolean

# Base = declarative_base()
# class ApartamentMySQL(Base):
#     __tablename__ = 'apartaments'
#     monthly_rent = mapped_column(Integer)
#     area = mapped_column(Integer)
#     additional_fees = mapped_column(Integer)
#     number_of_rooms = mapped_column(String(length=10))
#     deposit = mapped_column(Integer)
#     floor = mapped_column(String(length=20))
#     building_type = mapped_column(String(length=200))
#     available_from = mapped_column(String(length=200))
#     balcony_garden_terrace = mapped_column(String(length=200))
#     remote_service = mapped_column(String(length=200))
#     finishing_quality = mapped_column(String(length=200))
#     advertiser_type = mapped_column(String(length=200))
#     open_to_students = mapped_column(String(length=200))
#     furnishing = mapped_column(String(length=200))
#     utilities = mapped_column(String(length=200))
#     heating = mapped_column(String(length=200))
#     security = mapped_column(String(length=200))
#     windows = mapped_column(String(length=200))
#     elevator = mapped_column(String(length=200))
#     parking_space = mapped_column(String(length=200))
#     year_built = mapped_column(String(length=20))
#     building_material = mapped_column(String(length=200))
#     additional_info = mapped_column(String(length=200))
#     location = mapped_column(String(length=200))
#     title = mapped_column(String(length=200))
#     url = mapped_column(String(length=500),primary_key=True)
#     city = mapped_column(String(length=200))
#     county = mapped_column(String(length=200))
#     voivodeship = mapped_column(String(length=200))
#     district = mapped_column(String(length=200))
#     neighbourhood = mapped_column(String(length=200))
#     street = mapped_column(String(length=200))


# from cassandra.cqlengine.models import Model
# from cassandra.cqlengine import columns
# # Define the table structure for Cassandra
# class ApartamentCassandra(Model):
#     monthly_rent = columns.Integer()
#     area = columns.Integer()
#     additional_fees = columns.Integer()
#     number_of_rooms = columns.Text()
#     deposit = columns.Integer()
#     floor = columns.Text()
#     building_type = columns.Text()
#     available_from = columns.Text()
#     balcony_garden_terrace = columns.Text()
#     remote_service = columns.Text()
#     finishing_quality = columns.Text()
#     advertiser_type = columns.Text()
#     open_to_students = columns.Text()
#     furnishing = columns.Text()
#     utilities = columns.Text()
#     heating = columns.Text()
#     security = columns.Text()
#     windows = columns.Text()
#     elevator = columns.Text()
#     parking_space = columns.Text()
#     year_built = columns.Text()
#     building_material = columns.Text()
#     additional_info = columns.Text()
#     location = columns.Text()
#     title = columns.Text()
#     url = columns.Text(primary_key=True)
#     city = columns.Text()
#     county = columns.Text()
#     voivodeship = columns.Text()
#     district = columns.Text()
#     neighbourhood = columns.Text()
#     street = columns.Text()
