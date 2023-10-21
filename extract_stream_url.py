import os
import requests
#import sqlite3
import time
import random
from datetime import datetime
from sqlcipher3 import dbapi2 as sqlite

URL_TEMPLATE=os.environ['URL_TEMPLATE']
SITE_URL=os.environ['SITE_URL']
DB_ENCRYPTION_KEY=os.environ['DB_ENCRYPTION_KEY']

class Station:
    def __init__(self, row):
        self.id = row[0]
        self.place_id = row[1]
        self.title = row[2]
        self.url = row[3]
        self.stream_url = row[4]

    def update_db(self, cur):
        cur.execute(f"update stations set stream_url='{self.stream_url}' where id='{self.id}'")


def process_url(station):

    station_id = station.id
    timestamp = datetime.now().strftime("%s")
    initial_stream_url = URL_TEMPLATE.format(station_id=station_id, timestamp=timestamp)
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "Referer": f"{SITE_URL}{station.url}"
    }
    req = requests.head(initial_stream_url)
    if req.status_code != 302:
        print(f"URL {initial_stream_url} returned status code: {req.status_code}")
        return
    return req.next.url

db = sqlite.connect("radio-data.db")
db.execute(f'pragma key="{DB_ENCRYPTION_KEY}"')

cur = db.cursor()
cur.execute("select * from stations where stream_url='NONE' LIMIT 10")
rows = cur.fetchmany(size=10)

for row in rows:
    station = Station(row)
    print(station.id)
    stream_url = process_url(station)
    station.stream_url = stream_url
    station.update_db(cur)
    sleep_interval = random.randint(5, 10)
    print(f"Sleeping {sleep_interval} to prevent DDOSing")
    time.sleep(sleep_interval)

db.commit()
cur.close()

