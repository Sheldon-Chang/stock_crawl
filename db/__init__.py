from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Text, Float, Date
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('postgresql://postgres:password@localhost:5432/stock')
metadata = MetaData(engine)
DBsession = sessionmaker(bind=engine)
session = DBsession()
