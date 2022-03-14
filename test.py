from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from requests_html import HTMLSession

# session = HTMLSession()


# ua = 'Chrome/98.0.4758.102'
# header = {'User-agent': 'Chrome/98.0.4758.102',
#           'cookie': 'hblid=elMo8caF67nfdmip3h7B70H4LB6raklj; _hjid=bdccc90b-783d-40a6-bad1-d2bd17a1c96d; BID=D65188A6-5CDA-4879-84AD-EB13FCF598AB; _okdetect=%7B%22token%22%3A%2216244638555210%22%2C%22proto%22%3A%22https%3A%22%2C%22host%22%3A%22www.wantgoo.com%22%7D; olfsk=olfsk19333858063901221; _ok=8391-691-10-7433; _hjSessionUser_827061=eyJpZCI6ImM5OGRjMTY3LWNhODgtNTdkZi05NDU0LWUwZWMwNDY4MDE4MCIsImNyZWF0ZWQiOjE2Mzg2MjY4OTYxMTgsImV4aXN0aW5nIjp0cnVlfQ==; popup=showed; _smt_uid=62223fbb.60b0f3ed; BrowserMode=Web; _gcl_au=1.1.1934268919.1646411710; __cf_bm=IRW.76nb8KPb.NupTHKbPY7RBapJlERr6GxsYuxrDd0-1646585412-0-ASNXajK8+VwnZWZ63k1S1y9ZgKMD+OS+DZTJOGSaRBTnEZOGj0NlbslL7eaWalya68miOwRZSUxAzq7nruE7PdcqvNmw7vX0HQCbfGpdv+U4oA5Nks9c7Ez6DUMMATCDIw==; _gid=GA1.2.267694497.1646585411; client_fingerprint=708e1f50de59d5b5324847d3dbf03e1246d0cbbdfc1122bb591d2ab56134f367; wcsid=liulAi236BuwQtSI3h7B70H4DJB6Aba2; _okbk=cd4%3Dtrue%2Cvi5%3D0%2Cvi4%3D1646585413006%2Cvi3%3Dactive%2Cvi2%3Dfalse%2Cvi1%3Dfalse%2Ccd8%3Dchat%2Ccd6%3D0%2Ccd5%3Daway%2Ccd3%3Dfalse%2Ccd2%3D0%2Ccd1%3D0%2C; _hjSession_827061=eyJpZCI6IjZmOTZiNGE1LTUzM2UtNGVkNS04Mjk5LWIyYjA4NjM2NWY4OSIsImNyZWF0ZWQiOjE2NDY1ODU0MTcwNTEsImluU2FtcGxlIjpmYWxzZX0=; _hjIncludedInSessionSample=0; _hjAbsoluteSessionInProgress=0; _ga=GA1.2.314207498.1624463855; _ga_FCVGHSWXEQ=GS1.1.1646585411.12.1.1646586113.0; _oklv=1646586173204%2CliulAi236BuwQtSI3h7B70H4DJB6Aba2'}
#
# r = session.get('https://www.wantgoo.com/stock/3037/major-investors/main-trend', headers=header, verify=False)
# r.html.render(sleep=2)  # 首次使用，自動下載chromium
# # print(r.html.html)
# print(r.html.text)


import urllib
# import requests
# base_url = "https://www.wantgoo.com/stock/3037/major-investors/main-trend"
# url = base_url
# # header = {'User-agent': 'Chrome/98.0.4758.102',
# #           'cookie': 'hblid=elMo8caF67nfdmip3h7B70H4LB6raklj; _hjid=bdccc90b-783d-40a6-bad1-d2bd17a1c96d; BID=D65188A6-5CDA-4879-84AD-EB13FCF598AB; _okdetect=%7B%22token%22%3A%2216244638555210%22%2C%22proto%22%3A%22https%3A%22%2C%22host%22%3A%22www.wantgoo.com%22%7D; olfsk=olfsk19333858063901221; _ok=8391-691-10-7433; _hjSessionUser_827061=eyJpZCI6ImM5OGRjMTY3LWNhODgtNTdkZi05NDU0LWUwZWMwNDY4MDE4MCIsImNyZWF0ZWQiOjE2Mzg2MjY4OTYxMTgsImV4aXN0aW5nIjp0cnVlfQ==; popup=showed; _smt_uid=62223fbb.60b0f3ed; BrowserMode=Web; _gcl_au=1.1.1934268919.1646411710; __cf_bm=IRW.76nb8KPb.NupTHKbPY7RBapJlERr6GxsYuxrDd0-1646585412-0-ASNXajK8+VwnZWZ63k1S1y9ZgKMD+OS+DZTJOGSaRBTnEZOGj0NlbslL7eaWalya68miOwRZSUxAzq7nruE7PdcqvNmw7vX0HQCbfGpdv+U4oA5Nks9c7Ez6DUMMATCDIw==; _gid=GA1.2.267694497.1646585411; client_fingerprint=708e1f50de59d5b5324847d3dbf03e1246d0cbbdfc1122bb591d2ab56134f367; wcsid=liulAi236BuwQtSI3h7B70H4DJB6Aba2; _okbk=cd4%3Dtrue%2Cvi5%3D0%2Cvi4%3D1646585413006%2Cvi3%3Dactive%2Cvi2%3Dfalse%2Cvi1%3Dfalse%2Ccd8%3Dchat%2Ccd6%3D0%2Ccd5%3Daway%2Ccd3%3Dfalse%2Ccd2%3D0%2Ccd1%3D0%2C; _hjSession_827061=eyJpZCI6IjZmOTZiNGE1LTUzM2UtNGVkNS04Mjk5LWIyYjA4NjM2NWY4OSIsImNyZWF0ZWQiOjE2NDY1ODU0MTcwNTEsImluU2FtcGxlIjpmYWxzZX0=; _hjIncludedInSessionSample=0; _hjAbsoluteSessionInProgress=0; _ga=GA1.2.314207498.1624463855; _ga_FCVGHSWXEQ=GS1.1.1646585411.12.1.1646586113.0; _oklv=1646586173204%2CliulAi236BuwQtSI3h7B70H4DJB6Aba2'}

# request = urllib.request.Request(url, headers= header)
# html = urllib.request.urlopen(request).read().decode('utf-8')
# #
# soup = BeautifulSoup(html, features='lxml')
# print(soup)


# url = urllib.request.Request('https://www.wantgoo.com/stock/3037/major-investors/main-trend', headers = headers)
# html = urllib.request.urlopen(url).read()
# soup = BeautifulSoup(html, 'html.parser')

# s= Service(r'.\chromedriver.exe')
# opts = Options()
# opts.add_argument("user-agent='Chrome/98.0.4758.102'")
# driver = webdriver.Chrome(service=s, options=opts)
# driver.get('https://www.wantgoo.com/stock/3037/major-investors/main-trend', )
# try:
#     element = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.CLASS_NAME, "dn"))
#     )
# finally:
#     driver.quit()

# yahoo
# header = {'User-agent': 'Chrome/98.0.4758.102'}
# url = urllib.request.Request('https://tw.stock.yahoo.com/quote/{stock_id}/profile'.
#                              format(stock_id=1240), headers=header)
# html = urllib.request.urlopen(url).read()
# soup = BeautifulSoup(html, 'html.parser')
# item = soup.find_all('div', class_='Py(8px) Pstart(12px) Bxz(bb)')
# captial = int(int(item[14].text.replace(',', '')) / 100000000)
# shares = int(int(item[16].text.replace(',', '')) / 1000)
# print(captial,shares)




# tbody = soup.find('table', id='main-trend')
# for i in tbody:
#     item = i.find('tbody')
#     print(item, '\n===')
#     try:
#         rows = item.find_all('tr')
#         print(rows, '\n===')
#         for tr in rows:
#             col = tr.find_all('td')
#             print(col, '\n===')
#             for td in col:
#                 print(td.text, '\n===')
#     except:
#         print('no tbody')



# import asyncio
# from pyppeteer import launch
#
# async def main():
#     # 開啟瀏覽器程序
#     browser = await launch()
#     # 用瀏覽器連到 https://pythonclock.org/ 網站
#     page = await browser.newPage()
#     await page.setUserAgent(
#         'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3542.0 Safari/537.36')
#     await page.goto('https://www.wantgoo.com/stock/3037/major-investors/main-trend', {'waitUntil' : 'domcontentloaded'})
#     time.sleep(10)
#     html_doc = await page.content()
#     soup = BeautifulSoup(html_doc, 'lxml')
#
#     await browser.close()
#
#     print(soup)
#
# asyncio.set_event_loop(asyncio.new_event_loop())
# asyncio.get_event_loop().run_until_complete(main())


import pandas as pd
import yfinance as yf
import pprint
df = pd.read_csv('test.csv', encoding='cp950')['stock_id'].tolist()
a = ''
for i in df:
    a = a + ' ' + str(i)
data = yf.download(a ,start='2022-03-08', end='2022-03-08')
print(data)