import csv
from datetime import datetime
import json
import pytz

# set timezone and year
DEFAULT_TIMEZONE = pytz.timezone('America/Los_Angeles')
YEAR = 2018

data_of_year = []

def add_date(date):
    data_of_year.insert(0, dict(date=date, value=1))

def get_tweet_info(d):
    date = d.strftime('%-m/%-d/%-Y')
    if len(data_of_year) == 0:
        add_date(date)
    else:
        if data_of_year[0]['date'] == date:
            data_of_year[0]['value'] += 1
        else:
            add_date(date)

with open('tweets.csv', newline='') as csvfile:
    sheet = csv.DictReader(csvfile)
    for row in sheet:
        utc_date = datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S %z')
        date = utc_date.astimezone(DEFAULT_TIMEZONE)
        year = int(date.year)
        if year == YEAR:
            get_tweet_info(date)
        elif year < YEAR:
            break

# save data as json
fd = open('data-' + str(YEAR) + '.json', 'w', encoding='utf8')
json_data = json.dumps(data_of_year, separators=(',',':'), indent=2, ensure_ascii=False)
fd.write(json_data)
fd.close()
