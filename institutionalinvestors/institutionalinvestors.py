import pandas as pd
import requests
import time
from datetime import datetime, timedelta
from io import StringIO
from method.method import *
from db.method import *
import random


class InstitutionalInvestors:
    def __init__(self):
        self.twse_institutional_investors_url = 'https://www.twse.com.tw/fund/T86?response=csv&date='
        self.twse_deal_url = 'https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date='
        self.tpex_deal_url = 'http://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_download.php?l=zh-tw&d='
        self.tpex_institutional_investors_url = 'http://www.tpex.org.tw/web/stock/3insti/daily_trade/3itrade_hedge_result.php?l=zh-tw&o=csv&se=EW&t=D&d='   #BIGD
        self.stock_list = ''

    def get_day_stock_info(self):
        index = 0
        today = datetime.today()
        while index != 2:
            date = (today - timedelta(days=index)).strftime('%Y%m%d')

            index += 1
            twse_day = date
            tpex_day = tpex_date_changer(date)
            twse_ii_url = '{stock_url}{date}&selectType=ALLBUT0999'.format(
                stock_url=self.twse_institutional_investors_url, date=twse_day)
            twse_deal_url = '{volume_url}{date}&type=ALLBUT0999'.format(
                volume_url=self.twse_deal_url, date=twse_day)
            # get tpex url
            tpex_ii_url = '{stock_url}{date}&selectType=ALLBUT0999'.format(
                stock_url=self.tpex_institutional_investors_url, date=tpex_day)
            tpex_deal_url = '{volume_url}{date}&type=ALLBUT0999'.format(
                volume_url=self.tpex_deal_url, date=tpex_day)
            r = requests.get(twse_ii_url)
            time.sleep(5)
            if len(r.text) < 100:
                continue
            # get parsed info
            twse_ii_info = self.crawl_parse_url(twse_ii_url, date, 'twse_ii')
            time.sleep(5)
            twse_deal_info = self.crawl_parse_url(twse_deal_url, date, 'twse_deal')
            time.sleep(5)
            tpex_ii_info = self.crawl_parse_url(tpex_ii_url, date, 'tpex_ii')
            time.sleep(5)
            tpex_deal_info = self.crawl_parse_url(tpex_deal_url, date, 'tpex_deal')
            time.sleep(5)
            # get merge data
            twse_info = self.merge_data(twse_ii_info, twse_deal_info)
            tpex_info = self.merge_data(tpex_ii_info, tpex_deal_info)

            # concat data
            self.concat_data(twse_info, tpex_info)

    def merge_data(self, ii_info, deal_info):
        return pd.merge(deal_info, ii_info, on=['date', 'name', 'stock_id'], how='left').fillna(0)

    def concat_data(self, twse, tpex):
        df = pd.concat([twse, tpex], join='outer', ignore_index=True).sort_values(by=['stock_id']).fillna(0)
        #df.to_csv('test.csv', encoding='cp950')
        print(df)
        save_to_db(df)

    def crawl_parse_url(self, url, date, index):
        if index == 'twse_ii':
            r = requests.get(url)
            names = ['證券代號', '證券名稱', '外陸資買進股數(不含外資自營商)', '外陸資賣出股數(不含外資自營商)', '外陸資買賣超股數(不含外資自營商)',
                     '外資自營商買進股數', '外資自營商賣出股數', '外資自營商買賣超股數', '投信買進股數', '投信賣出股數', '投信買賣超股數',
                     '自營商買賣超股數', '自營商買進股數(自行買賣)', '自營商賣出股數(自行買賣)', '自營商買賣超股數(自行買賣)', '自營商買進股數(避險)',
                     '自營商賣出股數(避險)', '自營商買賣超股數(避險)', '三大法人買賣超股數', '']
            # 過濾非股票及說明文字
            df = pd.read_csv(StringIO(r.text), header=None, names=names).dropna(how='all', axis=1).dropna(how='any')
            df = df.drop(df.index[0])
            mask = (df['證券代號'].str.len() == 4) & (df['證券代號'].str[0] != '0')  # 過濾ETF及BC
            df = df.loc[mask]
            df = df[['證券代號', '證券名稱', '外陸資買賣超股數(不含外資自營商)',
                     '投信買賣超股數', '自營商買賣超股數', '自營商買賣超股數(避險)']]  # 只抓要的欄位
            df = df.rename(columns={'證券代號': 'stock_id',
                                    '證券名稱': 'name',
                                    '外陸資買賣超股數(不含外資自營商)': 'fi_overbuy',
                                    '投信買賣超股數': 'it_overbuy',
                                    '自營商買賣超股數': 'dealer_overbuy',
                                    '自營商買賣超股數(避險)': 'dealer_overbuy_avoid'})
            df = df.astype(str).apply(lambda s: s.str.replace(',', ''))   # 過濾逗號
            df = df.sort_values(by=['stock_id'])  # 排序
            stock_name = df['name']
            df = df.apply(lambda s: pd.to_numeric(s, errors='coerce')).dropna(how='all', axis=1)  # 名稱會不見
            df['date'] = date  # 填入時間
            df['fi_overbuy'] = df['fi_overbuy'].map(lambda x: do(x))
            df['it_overbuy'] = df['it_overbuy'].map(lambda x: do(x))
            df['dealer_overbuy'] = df['dealer_overbuy'].map(lambda x: do(x))
            df['dealer_overbuy_avoid'] = df['dealer_overbuy_avoid'].map(lambda x: do(x))
            df['name'] = stock_name  # 填入名稱
            df['name'] = df['name'].map(lambda x: x.replace(' ', ''))
            df = df[['date', 'stock_id', 'name', 'fi_overbuy',
                     'it_overbuy', 'dealer_overbuy', 'dealer_overbuy_avoid']]
            return df

        elif index =='twse_deal':
            r = requests.get(url)
            names = ['證券代號', '證券名稱', '成交股數', '成交筆數', '成交金額', '開盤價', '最高價', '最低價',
                     '收盤價', '漲跌(+/-)', '漲跌價差', '最後揭示買價', '最後揭示買量', '最後揭示賣價', '最後揭示賣量', '本益比', '']
            df = pd.read_csv(StringIO(r.text), header=None, names=names).dropna(how='all', axis=1).dropna(how='any')
            df = df.drop(df.index[0])
            mask = (df['證券代號'].str.len() == 4) & (df['證券代號'].str[0] != '0')  # 過濾ETF及BC
            df = df.loc[mask]
            df = df.sort_values(by=['證券代號'])  # 排序
            df = df[['證券代號', '證券名稱', '成交股數', '最高價', '最低價', '開盤價', '收盤價']]  # 只抓要的欄位
            df = df.rename(columns={'證券代號': 'stock_id',
                                    '證券名稱': 'name',
                                    '成交股數': 'volume',
                                    '最高價': 'highest_price',
                                    '最低價': 'lowest_price',
                                    '開盤價': 'open_price',
                                    '收盤價': 'end_price'})
            stock_name = df['name']
            df['volume'] = df['volume'].map(lambda x: x.replace(',', ''))
            df = df.apply(lambda s: pd.to_numeric(s, errors='coerce')).dropna(how='all', axis=1)
            df['date'] = date  # 填入時
            df['volume'] = df['volume'].map(lambda x: do(x))
            df['name'] = stock_name  # 填入名稱
            df['name'] = df['name'].map(lambda x: x.replace(' ', ''))
            df = df[['date', 'stock_id', 'name', 'volume',
                     'highest_price', 'lowest_price', 'open_price', 'end_price']]
            return df

        elif index =='tpex_ii':
            r = requests.get(url)
            names = ['代號', '名稱', '外資及陸資(不含外資自營商)-買進股數', '外資及陸資(不含外資自營商)-賣出股數', '外資及陸資(不含外資自營商)-買賣超股數',
                     '外資自營商-買進股數', '外資自營商-賣出股數', '外資自營商-買賣超股數', '外資及陸資-買進股數', '外資及陸資-賣出股數', '外資及陸資-買賣超股數',
                     '投信-買進股數', '投信-賣出股數', '投信-買賣超股數', '自營商(自行買賣)-買進股數', '自營商(自行買賣)-賣出股數', '自營商(自行買賣)-買賣超股數',
                     '自營商(避險)-買進股數', '自營商(避險)-賣出股數', '自營商(避險)-買賣超股數', '自營商-買進股數', '自營商-賣出股數',
                     '自營商-買賣超股數','三大法人買賣超股數合計', '']
            df = pd.read_csv(StringIO(r.text), header=None, names=names).dropna(how='all', axis=1).dropna(how='any')
            df = df.drop(df.index[0])
            mask = (df['代號'].str.len() == 4) & (df['代號'].str[0] != '0')  # 過濾ETF及BC
            df = df.loc[mask]
            df = df[['代號', '名稱', '外資及陸資(不含外資自營商)-買賣超股數',
                     '投信-買賣超股數', '自營商(自行買賣)-買賣超股數', '自營商(避險)-買賣超股數']]  # 只抓要的欄位
            df = df.rename(columns={'代號': 'stock_id',
                                    '名稱': 'name',
                                    '外資及陸資(不含外資自營商)-買賣超股數': 'fi_overbuy',
                                    '投信-買賣超股數': 'it_overbuy',
                                    '自營商(自行買賣)-買賣超股數': 'dealer_overbuy',
                                    '自營商(避險)-買賣超股數': 'dealer_overbuy_avoid'})
            df = df.astype(str).apply(lambda s: s.str.replace(',', ''))  # 過濾逗號
            df = df.sort_values(by=['stock_id'])  # 排序
            stock_name = df['name']
            df = df.apply(lambda s: pd.to_numeric(s, errors='coerce')).dropna(how='all', axis=1)  # 名稱會不見
            df['date'] = date  # 填入時間
            df['fi_overbuy'] = df['fi_overbuy'].map(lambda x: do(x))
            df['it_overbuy'] = df['it_overbuy'].map(lambda x: do(x))
            df['dealer_overbuy'] = df['dealer_overbuy'].map(lambda x: do(x))
            df['dealer_overbuy_avoid'] = df['dealer_overbuy_avoid'].map(lambda x: do(x))
            df['name'] = stock_name  # 填入名稱
            df['name'] = df['name'].map(lambda x: x.replace(' ', ''))
            df = df[['date', 'name', 'stock_id', 'fi_overbuy',
                     'it_overbuy', 'dealer_overbuy', 'dealer_overbuy_avoid']]
            return df
        else:
            r = requests.get(url)
            names = ['代號', '名稱', '收盤', '漲跌', '開盤', '最高', '最低', '均價', '成交股數', '成交金額(元)', '成交筆數',
                     '最後買價', '最後買量(千股)', '最後賣價', '最後賣量(千股)', '發行股數', '次日參考價', '次日漲停價', '次日跌停價', '']
            df = pd.read_csv(StringIO(r.text), header=None, names=names).dropna(how='all', axis=1).dropna(how='any')
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
            df.columns = df.columns.map(lambda x: x.replace(' ', ''))
            stock_name = df['name']
            df['volume'] = df['volume'].map(lambda x: x.replace(',', ''))
            df = df.apply(lambda s: pd.to_numeric(s, errors='coerce')).dropna(how='all', axis=1)
            df['date'] = date  # 填入時間
            df['volume'] = df['volume'].map(lambda x: do(x))
            df['name'] = stock_name  # 填入名稱
            df['name'] = df['name'].map(lambda x: x.replace(' ', ''))
            df = df[['date', 'name', 'stock_id', 'volume', 'highest_price', 'lowest_price', 'open_price', 'end_price']]
            return df


def do(x):
    try:
        res = int(x/1000)
        return res
    except:
        return 0

app = InstitutionalInvestors()
# app.crawl_parse_url(tpex_vol_url, '20220124', 'tpex_vol')
app.get_day_stock_info()

