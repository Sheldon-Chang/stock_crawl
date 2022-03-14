執行institutionalinvestors.py程式即可撈取股票資訊
資料庫使用的為postgresql + sqlachemy ORM

===========================================================
institutionalinvestors/institutionalinvestors.py

past_day表示撈取過去指定天數之股票內容

===========================================================

db/__init__.py

engine = create_engine('postgresql://ACCOUNT:ACCOUNT@IP:PORT/DB_NAME')
ACCOUNT為資料庫帳號
PASSWORD為資料庫密碼
IP為資料庫所在位置
PORT為資料庫port
DB_NAME為資料庫名稱

===========================================================

db/methods.py

engine = create_engine('postgresql://postgres:password@localhost:5432/stock')

ACCOUNT為資料庫帳號
PASSWORD為資料庫密碼
IP為資料庫所在位置
PORT為資料庫port
DB_NAME為資料庫名稱
