import pandas as pd
import codecs
from db.db_table import *
from db.method import *
from io import StringIO
import datetime
import pprint

original_file = 'C:\\Users\\csist\\Desktop\\1090853\\google\\stock_prac\\RSTA3104_1100125.csv'
pd.set_option('display.max_row', None, 'display.max_columns', None)
year = 2022
month = 1
day = 17
interval_time = 3
record_date = datetime.date(year, month, day)


def FileToUtf8(file, newfile):
    f = open(file, 'rb+')
    content = f.read()
    source_encoding = 'utf-8'
    try:
        content.decode('utf-8').encode('utf-8')
        source_encoding = 'utf-8'
    except:
        try:
            content.decode('gbk').encode('utf-8')
            source_encoding = 'gbk'
        except:
            try:
                content.decode('cp950').encode('utf-8')
                source_encoding = 'cp950'
            except:
                try:
                    content.decode('gb2312').encode('utf-8')
                    source_encoding = 'gb2312'
                except:
                    try:
                        content.decode('gb18030').encode('utf-8')
                        source_encoding = 'gb18030'
                    except:
                        try:
                            content.decode('big5').encode('utf-8')
                            source_encoding = 'big5'
                        except:
                            try:
                                content.decode('cp936').encode('utf-8')
                                source_encoding = 'cp936'
                            except Exception as e:
                                print(e)
    f.close()
    print(source_encoding)
    block_size = 4096
    with codecs.open(original_file, 'r', source_encoding) as f:
        with codecs.open(newfile, 'w', 'utf-8') as new_f:
            content = f.read()
            new_f.write(content)


def save(df):
    for index, data in df.iterrows():
        print('-----------')
        print(index, data['name'])
        if not exist_check(Stock.stock_id == data['stock_id']):
            print('new stock create table')
            new_stock = Stock(stock_id=data['stock_id'], name=data['name'])
            insert([new_stock])
            create_trade_table(data['stock_id'])
        # stock_dict = create_stock_dict(data['stock_id'])
        # new_stock_table = type('new_stock_table', (Base, ), stock_dict)
        # stock_data = new_stock_table(date='0125', stock_id=data['stock_id'], name=data['name'], volume=data['volume'],
        #                              highest_price=data['highest_price'], lowest_price=data['lowest_price'],
        #                              open_price=data['open_price'], end_price=data['end_price'])
        stock = stock_data(Base, data['stock_id'])
        tmp_data = stock(date=record_date, stock_id=data['stock_id'], name=data['name'], volume=data['volume'],
                         highest_price=data['highest_price'], lowest_price=data['lowest_price'],
                         open_price=data['open_price'], end_price=data['end_price'])
        if not exist_check(stock.date == tmp_data.date):
            print('insert new stock data')
            insert([tmp_data])
        else:
            print('update stock data')
            merge(tmp_data)


# FileToUtf8(original_file, 'test.csv')

# data_tmp = pd.read_csv(original_file, encoding='cp950').dropna(how='all', axis=1).dropna(how='any')  # 過濾非股票及說明文字
# data_tmp.dropna(how='all', axis=1).dropna(how='any')  # 過濾非股票及說明文字
# print(data_tmp)
# names_MI = ['證券代號','證券名稱','成交股數','成交筆數'	,'成交金額',	'開盤價'	,'最高價'	,'最低價'
#     ,'收盤價'	,'漲跌(+/-)'	,'漲跌價差',	'最後揭示買價',	'最後揭示買量',	'最後揭示賣價',	'最後揭示賣量',	'本益比']
# names = ['證券代號', '證券名稱', '外陸資買進股數(不含外資自營商)', '外陸資賣出股數(不含外資自營商)', '外陸資買賣超股數(不含外資自營商)',
#          '外資自營商買進股數', '外資自營商賣出股數', '外資自營商買賣超股數', '投信買進股數', '投信賣出股數', '投信買賣超股數',
#          '自營商買賣超股數', '自營商買進股數(自行買賣)', '自營商賣出股數(自行買賣)', '自營商買賣超股數(自行買賣)', '自營商買進股數(避險)',
#          '自營商賣出股數(避險)', '自營商買賣超股數(避險)', '三大法人買賣超股數']
# names_T86 = ['代號',	'名稱'	,'收盤' 	,'漲跌'	,'開盤' 	,'最高' 	,'最低'	,'均價' 	,'成交股數' , 	'成交金額(元)'	,'成交筆數' 	,'最後買價',
#          '最後買量(千股)'	,'最後賣價'	,'最後賣量(千股)'	,'發行股數' 	,'次日參考價', 	 '次日漲停價', 	'次日跌停價']
# names_BIGD = ['代號',	'名稱'	,'外資及陸資(不含外資自營商)-買進股數',	'外資及陸資(不含外資自營商)-賣出股數',	'外資及陸資(不含外資自營商)-買賣超股數',
#          '外資自營商-買進股數',	'外資自營商-賣出股數',	'外資自營商-買賣超股數'	,'外資及陸資-買進股數'	,'外資及陸資-賣出股數'	,'外資及陸資-買賣超股數',
#          '投信-買進股數'	,'投信-賣出股數'	,'投信-買賣超股數',	'自營商(自行買賣)-買進股數',	'自營商(自行買賣)-賣出股數',	'自營商(自行買賣)-買賣超股數',
#          '自營商(避險)-買進股數'	,'自營商(避險)-賣出股數'	,'自營商(避險)-買賣超股數'	,'自營商-買進股數',	'自營商-賣出股數',	,
#         '自營商-買賣超股數	三大法人買賣超股數合計']
names_RSTA = ['代號', '名稱', '收盤', '漲跌', '開盤', '最高', '最低', '均價', '成交股數', '成交金額(元)', '成交筆數', '最後買價',
                     '最後買量(千股)', '最後賣價', '最後賣量(千股)', '發行股數', '次日參考價', '次日漲停價', '次日跌停價']
df = pd.read_csv(original_file, header=None, names=names_RSTA, encoding='cp950').dropna(how='all', axis=1)\
    .dropna(how='any')
df = df.drop(df.index[0])
mask = (df['代號'].str.len() == 4) & (df['代號'].str[0] != '0')  # 過濾ETF及BC
df = df.loc[mask]
df = df.sort_values(by=['代號'])  # 排序
df = df[['名稱', '代號', '成交股數', '最高', '最低', '開盤', '收盤']]  # 只抓要的欄位
df = df.rename(columns={'名稱': 'name',
                        '代號': 'stock_id',
                        '成交股數': 'volume',
                        '最高': 'highest_price',
                        '最低': 'lowest_price',
                        '開盤': 'open_price',
                        '收盤': 'end_price'})

# create_stock_table()
save(df)

# stock = stock_data(Base, '1240')
# target_list = query_filter(stock, stock.date <= '2022-01-20')
# target_list = query_filter(stock, stock.date > record_date - datetime.timedelta(days=interval_time))
target_list = get_history_record(1240, 3)
for target in target_list:
    pprint.pprint(vars(target))


def read_data(date):
    file_BIGD = 'BIGD_111' + date + '.csv'
    file_MI = 'MI_INDEX_ALLBUT0999_2022' + date + '.csv'
    file_RSTA = 'RSTA3104_110' + date + '.csv'
    file_T86 = 'T86_ALLBUT0999_2022' + date + '.csv'
    names_MI = ['證券代號', '證券名稱', '成交股數', '成交筆數', '成交金額', '開盤價', '最高價', '最低價', '收盤價', '漲跌(+/-)',
                '漲跌價差', '最後揭示買價', '最後揭示買量', '最後揭示賣價', '最後揭示賣量', '本益比']
    names_T86 = ['代號', '名稱', '收盤', '漲跌', '開盤', '最高', '最低', '均價', '成交股數', '成交金額(元)', '成交筆數', '最後買價',
                 '最後買量(千股)', '最後賣價', '最後賣量(千股)', '發行股數', '次日參考價', '次日漲停價', '次日跌停價']
    names_BIGD = ['代號', '名稱', '外資及陸資(不含外資自營商)-買進股數', '外資及陸資(不含外資自營商)-賣出股數',
                  '外資及陸資(不含外資自營商)-買賣超股數', '外資自營商-買進股數', '外資自營商-賣出股數', '外資自營商-買賣超股數',
                  '外資及陸資-買進股數', '外資及陸資-賣出股數', '外資及陸資-買賣超股數', '投信-買進股數', '投信-賣出股數',
                  '投信-買賣超股數',	'自營商(自行買賣)-買進股數',	'自營商(自行買賣)-賣出股數', '自營商(自行買賣)-買賣超股數',
                  '自營商(避險)-買進股數', '自營商(避險)-賣出股數', '自營商(避險)-買賣超股數', '自營商-買進股數',	'自營商-賣出股數',
                  '自營商-買賣超股數	三大法人買賣超股數合計']
    names_RSTA = ['代號', '名稱', '收盤', '漲跌', '開盤', '最高', '最低', '均價', '成交股數', '成交金額(元)', '成交筆數', '最後買價',
                  '最後買量(千股)', '最後賣價', '最後賣量(千股)', '發行股數', '次日參考價', '次日漲停價', '次日跌停價']


