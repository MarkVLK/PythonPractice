#!/usr/bin/env python

from __future__ import print_function

import contextlib
import re
import requests
import sys
import urllib

CAR_DICT = {'Acura': 2, 'Alfa Romeo': 3, 'Aston Martin': 54, 'Audi': 4,
        'Bentley': 57, 'BMW': 5, 'Buick': 7, 'Cadillac': 8, 'Chevrolet': 9,
        'Chrysler': 10, 'Dodge': 13, 'Ferrari': 397, 'FIAT': 430,
        'Ford': 15, 'Freightliner': 867, 'GMC': 16, 'Honda': 18,
        'Hyundai': 20, 'Infiniti': 21, 'Jaguar': 23, 'Jeep': 24, 'Kia': 25,
        'Lamborghini': 59, 'Land Rover': 26, 'Lexus': 27, 'Lincoln': 28,
        'Lotus': 55, 'Maserati': 61, 'Mazda': 30, 'McLaren': 799,
        'Mercedes-Benz': 31, 'MINI': 29, 'Mitsubishi': 34, 'Nissan': 35,
        'Porsche': 41, 'Ram': 783, 'Rolls-Royce': 58, 'Scion': 45,
        'smart': 507, 'SRT': 849, 'Subaru': 47, 'Tesla': 834, 'Toyota': 49,
        'Volkswagen': 50, 'Volvo': 51}

MODEL_REQ_URL = 'http://www.kbb.com/jsdata/3.1.85.2_53460/_modelsyears?\
        vehicleclass=NewCar&makeid=%d&filterbycpo=false&filter=&priceMin=&\
        priceMax=&categoryId=0&includeDefaultVehicleId=false&\
        includeTrims=false&hasNCBBPrice=false'

make = raw_input('Enter car make: ').title()

if make in CAR_DICT:
    makeid = CAR_DICT[make]
else:
    print('Invalid make!')
    sys.exit(0)

# Get models
print('Requesting models...')
r = requests.get(MODEL_REQ_URL % makeid)
data = r.json()
model_dict = {}
print('Storing models...')
for i, val in enumerate(data):
    model_dict[val['Name']] = val['Year']

model = raw_input('Enter a %s model: ' % make).title()
if model in model_dict.keys():
    year = int(raw_input('Enter a year %s: ' % model_dict[model]))
    if year in model_dict[model]:
        KBB_URL = 'http://www.kbb.com/%s/%s/%d/categories/?intent=buy-new'\
                % (make, model, year)
    else:
        print('Invalid year!')
        sys.exit(0)
else:
    print('Invalid model!')
    sys.exit(0)

print('Requesting page...')
r = requests.get(KBB_URL)
print('Writing HTML...')
with open('kbb.html', 'w') as f:
    f.write(r.text.encode('ascii', 'ignore'))

style_patt = r'<div class="style-name section-title">\s*(\S*)\s*'
data = r.text
m = re.search(style_patt, data)
if m:
    for i in range(1, len(m.groups())+1):
        print(m.group(i))


'''
# Get style/trim
with contextlib.closing(urllib.urlopen(MODEL_REQ_URL % makeid)) as f:
    data = f.read()
    m = re.search(style_patt, data)
    if m:
        style = m.group(1)

    title_match = re.search(TITLE_PATT, return_data)
    title = title_match.group(1) if title_match is not None else '(not available)'

    print('Rank:\t', rank)
'''
