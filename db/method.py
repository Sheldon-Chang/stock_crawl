from db.models import *
from db.db_table import *
from sqlalchemy import Column, Integer, Text, Float, exists
from datetime import datetime, timedelta
import urllib
from bs4 import BeautifulSoup
import time

engine = create_engine('postgresql://ACCOUNT:PASSWORD@IP:PORT/DB_NAME')
db = declarative_base()
metadata = MetaData(engine)
DBsession = sessionmaker(bind=engine)
session = DBsession()


class StockQuery:
    def __init__(self, model, session):
        self.model = model
        self.session = session

    def add(self, item):
        self.session.add_all([item])
        self.session.commit()
        self.session.close()

    def query_all(self):
        return self.session.query(self.model).all()

    def query_filter(self, query):
        return self.session.query(self.model).filter(query).all()

    def update(self, query, update_content):
        self.session.query(self.model).filter(query).update(update_content)
        self.session.commit()
        self.session.close()

    def delete(self, query):
        self.session.query(self.model).filter(query).delete()
        self.session.commit()
        self.session.close()

    def exist(self, column, content):
        q = self.session.query(self.model).filter(column=content)
        return self.session.query(q.exists()).scalar()


def check_table_exist(conn, table):
    if table in conn.engine.table_names():
        return True
    else:
        return False


def insert(models):
    try:
        session.add_all(models)
        session.commit()
        session.close()
    except Exception as e:
        print('DatabaseManager insert error.', e)
        raise e
    return


def delete(models, filters):
    try:
        target = db.session.query(models).filter(filters)
        session.delete(target)
        session.commit()
        session.close()
    except Exception as e:
        print('DatabaseManager delete error.', e)
        raise e
    return


def merge(models):
    try:
        session.merge(models)
        session.commit()
        session.close()
    except Exception as e:
        print('DatabaseManager merge error.', e)
        raise e
    return


def query(models):
    try:
        result = session.query(models).all
    except Exception as e:
        print('DatabaseManager query error', e)
        raise e
    return result


def query_filter_and_update(models, id, update):
    try:
        result = session.query(models).filter_by(stock_id=id).update(update)
        print('result')
        session.commit()
        session.close()
    except Exception as e:
        print('DatabaseManager query_filter error', e)
        raise e
    return result


def exist_check(filters):
    try:
        result = session.query(exists().where(filters)).scalar()
        session.commit()
        session.close()
        # print('DatabaseManager exist_check : ', result)
        return result
    except Exception as e:
        print('DatabaseManager exist_check error', e)
        return e


def save_to_db(df):
    create_stock_table()
    for index, data in df.iterrows():
        if not exist_check(Stock.stock_id == data['stock_id']):
            captial, shares, catalog = get_stock_profile(data['stock_id'])
            if captial == 0:
                continue
            new_stock = Stock(stock_id=data['stock_id'], name=data['name'],
                              captial=captial, shares=shares, catalog=catalog)
            insert([new_stock])
            create_trade_table(data['stock_id'])
        stock = stock_data(Base, data['stock_id'])
        
#         captial, shares, catalog = get_stock_profile(data['stock_id'])
#         print('here 1', captial, shares, catalog)
#         query_filter_and_update(Stock, data['stock_id'], {'catalog': catalog})

#         trend_overbuy, trend_overbuy_propotion = get_stock_trend(data['stock_id'])
#         tmp_data = stock(date=data['date'], stock_id=data['stock_id'], name=data['name'], volume=data['volume'],
#                          highest_price=data['highest_price'], lowest_price=data['lowest_price'],
#                          open_price=data['open_price'], end_price=data['end_price'],
#                          fi_overbuy=data['fi_overbuy'], it_overbuy=data['it_overbuy'],
#                          dealer_overbuy=data['dealer_overbuy'], dealer_overbuy_avoid=data['dealer_overbuy_avoid'],
#                          trend_overbuy=trend_overbuy, trend_overbuy_propotion=trend_overbuy_propotion)

        tmp_data = stock(date=data['date'], stock_id=data['stock_id'], name=data['name'], volume=data['volume'],
                         highest_price=data['highest_price'], lowest_price=data['lowest_price'],
                         open_price=data['open_price'], end_price=data['end_price'],
                         fi_overbuy=data['fi_overbuy'], it_overbuy=data['it_overbuy'],
                         dealer_overbuy=data['dealer_overbuy'], dealer_overbuy_avoid=data['dealer_overbuy_avoid'])
        if not exist_check(stock.date == data['date']):
            insert([tmp_data])
        else:
            merge(tmp_data)


def get_history_record(stock_id, time_interval, date=None):
    stock = stock_data(Base, str(stock_id))
    try:
        if not date:
            target_list = session.query(stock).filter(stock.date > date(2022, 1, 25)
                                                      - timedelta(days=time_interval))
        else:
            target_list = session.query(stock).filter(stock.date >= date)
        return target_list

    except Exception as e:
        print('DatabaseManager get_history_record', e)
        return e


def get_stock_profile(stock_id):
    header = {'User-agent': 'Chrome/98.0.4758.102'}
    try:
        url = urllib.request.Request('https://tw.stock.yahoo.com/quote/{stock_id}/profile'.
                                     format(stock_id=stock_id), headers=header)
        html = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html, 'html.parser')
        item = soup.find_all('div', class_='Py(8px) Pstart(12px) Bxz(bb)')
        captial = int(int(item[14].text.replace(',', '')) / 100000000)
        shares = int(int(item[16].text.replace(',', '')) / 1000)
        catalog = item[8].text
        # time.sleep(10)
        return captial, shares, catalog
    except Exception as e:
        return 0, 0


def get_stock_trend(stock_id):
    header = {'User-agent': 'Chrome/98.0.4758.102'}
    try:
        url = urllib.request.Request('https://tw.stock.yahoo.com/quote/{stock_id}/broker-trading'.
                                     format(stock_id=stock_id), headers=header)
        html = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html, 'html.parser')
        trend_item = soup.find_all('div', class_='D(f) Ai(c) Fld(c) W(100%)')
        trend_overbuy = trend_item[0].find_all('div')[1].text.replace(',', '')
        trend_overbuy_propotion = trend_item[3].find_all('div')[1].text.replace('%', '')
        # time.sleep(10)
        return trend_overbuy, trend_overbuy_propotion

    except Exception as e:
        return 0, 0


