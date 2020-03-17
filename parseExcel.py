import os
import PIL
from PIL import Image

import requests
import xlrd
import glob

url = 'http://www.pillicapture.com/api/createProduct/'
add_product_amount_url = 'http://www.pillicapture.com/api/addProductAmount/'

workbook = xlrd.open_workbook('tablets.xlsx')

worksheet = workbook.sheet_by_index(0)

brand = 'Fitwelpharma'

def deleteSpacesAndEmptyElements(array):
    array = list(filter(None, array))

    for i in range(len(array)):
        array[i] = array[i].replace('\n', '')

    return array


product_names = deleteSpacesAndEmptyElements(worksheet.col_values(2, 3, 272))
product_compositions = deleteSpacesAndEmptyElements(worksheet.col_values(3, 3, 272))
product_prices = list(filter(None, worksheet.col_values(6, 3, 272)))

# files = {'main_photo': open('test.png', 'rb')}
path = 'D:\Загрузки\wetransfer-1fcffd\Fitwel photos'

for i in range(0, len(product_names)):

    data = {
        'medicine_name': product_names[i],
        'price': product_prices[i],
        'main_component': product_compositions[i],
        'diseases': 1,
        'brand': brand,
        'discount': 0,
        'specialDiscount': 0,
        'creator': 5
    }
    files = None

    for filename in os.listdir(path):

        bracket_position = [pos for pos, char in enumerate(product_names[i]) if char == '(']

        try:
            productname = product_names[i][0:bracket_position[0]].replace('-', ' ')
        except IndexError:
            pass

        if productname.lower() in filename.lower():
            files = {'main_photo': open(path + "\\" + filename, 'rb')}

    r = requests.post(url=url, files=files, data=data, headers=dict(Referer=url))

    amount_data = {
        'product': product_names[i],
        'details_amount': 1000,
        'pharmacy': 2,

    }

    p = requests.post(url=add_product_amount_url, data=amount_data, headers=dict(Referer=url))
