#/usr/bin/python3

import json
import requests
import sqlite3
import datetime

# path to the database
db_path = '/home/pi/beer-sensors/dashboard/beer_sensors.db'

# querrying the TTN data integration
url = "https://binarybeer.data.thethingsnetwork.org/api/v2/query"
headers = {'Accept': 'application/json', 'Authorization': 'key ttn-account-v2.....'}
params = {'last': '1d'}
r = requests.get(url, headers=headers,params=params)

# Extracting the data
data = list()

try:
    data = json.loads(r.text)
except:
    print("No new data!")

# Pushing it to a SQLITE3 database

# ... opening the connection
conn = sqlite3.connect(db_path)
curs = conn.cursor()

# ... extracting the data
for r in data:
    weight     = r['val'] 
    lat        = -34.4062924
    lon        = 150.8813907
    keg_id     = r['device_id']
    time_stamp = r['time']

    # ... formatting the time stamp
    time_stamp_datetime = datetime.datetime.strptime(time_stamp[:-4],"%Y-%m-%dT%H:%M:%S.%f")
    time_stamp_fmt      = time_stamp_datetime.strftime("%Y-%m-%d %H:%M:%S")
   
    # Pushing it to the database
    try:
        curs.execute("""INSERT INTO beer values((?), (?), (?), (?), (?))""", 
                     (time_stamp_fmt, keg_id, weight, lat, lon))
    except sqlite3.IntegrityError as e:
        print("Could not insert record in the db:")
        print("  " + str(e))

# ... commiting the query and closing the connection
conn.commit()
conn.close()

