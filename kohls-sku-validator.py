#!/usr/bin/python

'''
This was written to scrape Kohls.com to validate
SKUs.
'''

import requests
import re

URL = 'https://www.kohls.com/search.jsp?submit-search=web-regular&search='
HEADERS = {
        'authority': 'www.kohls.com', 
        'upgrade-insecure-requests': '1',
        'dnt': '1', # For the lulz
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'referer': 'https://www.google.com',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9'
}

skus = dict()

# Example SKU List
#sku_list = [ '98556741', '99665071', '81019438', '46281768', '37292489', '37292488', '61404371', '54235788', '99605317', '99605273', '99605420', '87928677', '88605753', '91540323', '52892001', '73060942', '55786140', '27593052', '61501090', '91539158' ]

sku_list = []

def get_sku(sku):
    temp = list()
    r = requests.get('{}{}'.format(URL, sku), headers=HEADERS)
    match_name = re.search('itemprop="name" content="(.*?)"', r.text)
    match_sku = re.search('itemprop="sku" content="(.*?)"', r.text)
    if match_name:
            temp.append(match_name.group(1))
    else:
            temp.append('Name Not Found')

    if match_sku:
            temp.append(match_sku.group(1))
    else:
            temp.append('Sku Not Found')

    skus[sku] = temp

for sku in sku_list:
    get_sku(sku)

print skus
