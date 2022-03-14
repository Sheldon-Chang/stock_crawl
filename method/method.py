def tpex_date_changer(date):

    year = date[:4]
    year = str(int(year)-1911)
    month = date[4:6]
    day = date[6:]

    return year+"/"+month+"/"+day

