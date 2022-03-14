from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Text, Float, Date, JSON
from sqlalchemy.orm import sessionmaker
from . import *


def create_stock_table():
    Table('Stock', metadata,
          Column('stock_id', Integer, primary_key=True),
          Column('name', Text),
          Column('captial', Integer),
          Column('shares', Integer),
          Column('catalog', Text))
    metadata.create_all(engine)


def create_trade_table(table_name):
    Table(table_name, metadata,
          Column('date', Date, primary_key=True),
          Column('stock_id', Text),
          Column('name', Text),
          Column('fi_overbuy', Integer, nullable=True),
          Column('it_overbuy', Integer, nullable=True),
          Column('dealer_overbuy', Integer, nullable=True),
          Column('dealer_overbuy_avoid', Integer, nullable=True),
          Column('volume', Text, nullable=True),
          Column('highest_price', Float, nullable=True),
          Column('lowest_price', Float, nullable=True),
          Column('open_price', Float, nullable=True),
          Column('end_price', Float, nullable=True),
          )
    metadata.create_all(engine)
