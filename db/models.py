from sqlalchemy import Column, Integer, Text, Float, Date
from . import Base


class Stock(Base):

    def __init__(self, stock_id, name, captial, shares, catalog):
        self.stock_id = stock_id
        self.name = name
        self.captial = captial
        self.shares = shares
        self.catalog = catalog

    __tablename__ = 'Stock'
    stock_id = Column(Integer, primary_key=True)
    name = Column(Text)
    captial = Column(Integer)
    shares = Column(Integer)
    catalog = Column(Text)


# def stock_data(Base, tablename):
#     class StockData(Base):
#         def __init__(self, date, stock_id, name=None, volume=None, highest_price=None, lowest_price=None,
#                      open_price=None, end_price=None, fi_overbuy=None, it_overbuy=None, dealer_overbuy=None,
#                      dealer_overbuy_avoid=None, trend_overbuy=None, trend_overbuy_propotion=None):
#             self.date = date
#             self.stock_id = stock_id
#             self.name = name
#             self.volume = volume
#             self.highest_price = highest_price
#             self.lowest_price = lowest_price
#             self.open_price = open_price
#             self.end_price = end_price
#             self.fi_overbuy = fi_overbuy
#             self.it_overbuy = it_overbuy
#             self.dealer_overbuy = dealer_overbuy
#             self.dealer_overbuy_avoid = dealer_overbuy_avoid
#             self.trend_overbuy = trend_overbuy
#             self.trend_overbuy_propotion = trend_overbuy_propotion
#         __tablename__ = tablename
#         __table_args__ = {'extend_existing': True}
#         date = Column(Date, primary_key=True)
#         stock_id = Column(Integer)
#         name = Column(Text)
#         volume = Column(Text, nullable=True)
#         highest_price = Column(Float, nullable=True)
#         lowest_price = Column(Float, nullable=True)
#         open_price = Column(Float, nullable=True)
#         end_price = Column(Float, nullable=True)
#         fi_overbuy = Column(Integer, nullable=True)
#         it_overbuy = Column(Integer, nullable=True)
#         dealer_overbuy = Column(Integer, nullable=True)
#         dealer_overbuy_avoid = Column(Integer, nullable=True)
#         trend_overbuy = Column(Integer, nullable=True)
#         trend_overbuy_propotion = Column(Float, nullable=True)
#     return StockData


def stock_data(Base, tablename):
    class StockData(Base):
        def __init__(self, date, stock_id, name=None, volume=None, highest_price=None, lowest_price=None,
                     open_price=None, end_price=None, fi_overbuy=None, it_overbuy=None, dealer_overbuy=None,
                     dealer_overbuy_avoid=None):
            self.date = date
            self.stock_id = stock_id
            self.name = name
            self.volume = volume
            self.highest_price = highest_price
            self.lowest_price = lowest_price
            self.open_price = open_price
            self.end_price = end_price
            self.fi_overbuy = fi_overbuy
            self.it_overbuy = it_overbuy
            self.dealer_overbuy = dealer_overbuy
            self.dealer_overbuy_avoid = dealer_overbuy_avoid
        __tablename__ = tablename
        __table_args__ = {'extend_existing': True}
        date = Column(Date, primary_key=True)
        stock_id = Column(Integer)
        name = Column(Text)
        volume = Column(Text, nullable=True)
        highest_price = Column(Float, nullable=True)
        lowest_price = Column(Float, nullable=True)
        open_price = Column(Float, nullable=True)
        end_price = Column(Float, nullable=True)
        fi_overbuy = Column(Integer, nullable=True)
        it_overbuy = Column(Integer, nullable=True)
        dealer_overbuy = Column(Integer, nullable=True)
        dealer_overbuy_avoid = Column(Integer, nullable=True)
    return StockData


def create_stock_dict(stock_id):
    stock_dict = {'__tablename__': stock_id,
                  'stock_id': Column(Integer, primary_key=True),
                  'name': Column(Text),
                  'date': Column(Date),
                  'volume': Column(Text),
                  'highest_price': Column(Float),
                  'lowest_price': Column(Float),
                  'open_price': Column(Float),
                  'end_price': Column(Float),
                  'fi_overbuy': Column(Integer),
                  'it_overbuy': Column(Integer),
                  'dealer_overbuy': Column(Integer),
                  'dealer_overbuy_avoid': Column(Integer)}
    return stock_dict



