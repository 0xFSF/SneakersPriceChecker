import os
from openpyxl import Workbook
from selenium import webdriver
from prices import Prices
import pandas as pd
from size_converter import Size


def data():
    # Loads data from txt
    with open('data.txt', 'r') as file:
        txt = file.readlines()
    a = txt[0]
    b = txt[1]
    c = float(txt[2].replace("\n", ''))
    d = float(txt[3].replace("\n", ''))
    f = float(txt[4].replace("\n", ''))
    g = float(txt[5].replace("\n", ''))
    return [a, b, c, d, f, g]


def shoes(emai, passw, gbp, eur, usd, diff, name, driv, t):
    # Gets all needed data from sites
    df = pd.DataFrame(columns=['Product_name', 'SKU', 'Size', 'Stockx_payout', 'Klekt_payout', 'Restocks_payout',
                               'Goat_payout', 'Stockx_price', 'Klekt_price', 'Restocks_price', 'Goat_price', 'Site',
                               'Max_ZL', 'Max'])
    excel = pd.read_excel('shoes.xlsx', sheet_name=name)

    # Based on each row in excel sheet
    for index, row in excel.iterrows():
        if '.0' in str(row['size']):
            size = str(row['size']).replace('.0', '')
        else:
            size = str(row['size'])
        sku = row['sku']
        value = row['price']
        typ = row['type']
        converter = Size(size, row['sku'])
        sizes_list = converter.sizes()

        prices = Prices(driv, sizes_list, sku, emai, passw, t, gbp, eur, usd)
        stockx = prices.stockx()
        item_name = stockx[0]
        price1 = stockx[1]
        price_stockx = stockx[2]

        # klekt = prices.klekt()
        # price2 = klekt[0]
        # price_klekt = klekt[1]
        price2 = 0
        price_klekt = 0

        restocks = prices.restocks()
        price3 = restocks[0]
        price_restocks = restocks[1]

        # goat = prices.goat()
        # price4 = goat[0]
        # price_goat = goat[1]
        price4 = 0
        price_goat = 0

        # Calculates max_price and best sites based on given difference
        t += 1
        site = ''
        sites = {price_stockx: 'Stockx', price_klekt: 'Klekt', price_restocks: 'Restocks', price_goat: 'Goat'}
        if typ == 'Faktura':
            income_stockx = price_stockx - (value / 1.23)
            income_klekt = price_klekt - value + (value - (value / 1.23) - price_klekt + (price_klekt / 1.21))
            income_restocks = price_restocks - value + (value - (value / 1.23) - price_restocks + (price_restocks / 1.21
                                                                                                   ))
            income_goat = price_goat - value + (value - (value / 1.23) - price_goat + (price_goat / 1.21))
            prices = {income_stockx: price_stockx, income_klekt: price_klekt, income_restocks: price_restocks,
                      income_goat: price_goat}
            incomes = [income_stockx, income_klekt, income_restocks, income_goat]
            max_income = max(incomes)
            max_price = prices[max_income]
            for k in incomes:
                if max_income - k <= diff:
                    if site == '':
                        site = str(sites[prices[k]])
                    else:
                        site = site+'/'+str(sites[prices[k]])
        else:
            prices = [price_stockx, price_klekt, price_restocks, price_goat]
            max_price = max(prices)
            for n in prices:
                if max_price - n <= diff:
                    if site == '':
                        site = str(sites[n])
                    else:
                        site = site+'/'+str(sites[n])
        max_site = 0
        if site == 'Stockx':
            max_site = price_stockx
        if site == 'Restocks':
            max_site = price_restocks
        if site == 'Goat':
            max_site = price_goat

        new_row = {'Product_name': item_name, 'SKU': sku, 'Size': str(row['size']), 'Stockx_payout': str(price_stockx),
                   'Klekt_payout': str(price_klekt), 'Restocks_payout': str(price_restocks),
                   'Goat_payout': str(price_goat), 'Stockx_price': str(price1), 'Klekt_price': str(price2),
                   'Restocks_price': str(price3), 'Goat_price': str(price4), 'Site': site, 'Max_ZL': str(max_price),
                   'Max': str(max_site)}
        df = df.append(new_row, ignore_index=True)
        print('\n'+item_name)
        print(sku)
        print(row['size'])
        print({'Stockx: ': price_stockx, 'Klekt; ': price_klekt, 'Restocks: ': price_restocks, 'Goat: ': price_goat})

    return df


print('data.txt:\n'
      '1. Put stockx email\n'
      '2. Put stockx password\n'
      '3. Put GBP exchange rate with "." format\n'
      '4. Put EUR exchange rate with "." format\n'
      '5. Put USD exchange rate with "." format\n'
      '6. Put your difference between best prices\n'
      '\n'
      'shoes.xlsx:\n'
      '1. Put sku\n'
      "2. Put sizes into that format:\n"
      "Men - e.g. 9/9.5\n"
      "Women - e.g. 9W/9.5W\n"
      "Gs - e.g. 6Y/6.5Y\n"
      '3. Put price with "." format\n'
      '4. Put "Faktura" if you pay vat\n'
      '\n'
      'Write anything if you want to start\n')
input()

try:
    os.remove("stock.xlsx")
except FileNotFoundError:
    pass
wb = Workbook()
wb.save(filename='stock.xlsx')
data = data()
email = data[0]
password = data[1]
kurs_gbp = data[2]
kurs_eur = data[3]
kurs_usd = data[4]
difference = data[5]
sheets = pd.ExcelFile('shoes.xlsx').sheet_names
driver = webdriver.Chrome("C:/Users/dratw/Documents/Projekty/priceCompare/chromedriver.exe")
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source":
        "const newProto = navigator.__proto__;"
        "delete newProto.webdriver;"
        "navigator.__proto__ = newProto;"
    })

# Based on each sheet in excel file
for i in range(len(pd.ExcelFile('shoes.xlsx').sheet_names)):
    if i == 0:
        stock = shoes(email, password, kurs_gbp, kurs_eur, kurs_usd, difference, i, driver, i)
    else:
        stock = shoes(email, password, kurs_gbp, kurs_eur, kurs_usd, difference, i, driver, 1)
    with pd.ExcelWriter('stock.xlsx', engine='openpyxl', mode='a') as writer:
        stock.to_excel(writer, sheet_name=sheets[i])

writer.save()
writer.close()
