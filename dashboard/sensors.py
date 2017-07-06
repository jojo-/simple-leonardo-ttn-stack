#!/usr/bin/python3

#########################################################
# Simple dashboard for the Binary Beer project          #
#                                                       #
# Author: J. Barthelemy - SMART Infrastructure Facility #
# Version: 17 apr 2017                                  #
#########################################################

from flask import Flask, request, render_template
import datetime
import json
import sqlite3

# Path to data obtained from the TTN data integration
db_path   = '/home/pi/beer-sensors/dashboard/beer_sensors.db'
# Path to data obtained from the TTN HTTP integration
json_path = '/home/pi/beer-sensors/dashboard/beer_data_http.json'

app = Flask(__name__)
app.debug = True

@app.route("/track_data", methods=['GET'])
def beer_show_db():
    '''
    Getting the data from the TTN data integration
    '''

    try:
        keg_id = request.args['keg_id'];
    except:
        keg_id = "lora_module"
        
    records = get_beer_latest_record(keg_id);
    
    return render_template('smart_keg.html', records = records)


def get_beer_latest_record(keg_id):
    '''
    Querrying the database obtained from the TTN data integration

    param : keg_id - the id of the keg for which we want to obtain the data
    '''
    
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()
    curs.execute("select max(date_time), keg_id, weight, latitude, longitude \
                  from beer \
                  where keg_id = ?", (keg_id,))
    records = curs.fetchall()
    conn.close()
    
    return records

@app.route("/track_http", methods=['GET'])
def beer_show_json():
   '''
   Showing the data for the last record pushed by the TTN http integration
   '''

   # opening the file with the json-formatted data
   with open(json_path) as data_file:
     data = json.load(data_file) 

   # extracting the data
   keg_id     = data['dev_id']
   val        = data['payload_fields']['val']
   time_stamp = data['metadata']['time']
   rssi       = data['metadata']['gateways'][0]['rssi']
   lat        = -34.4062924
   lon        = 150.8813907

   # formatting the timestamp
   time_stamp_datetime = datetime.datetime.strptime(time_stamp[:-4],"%Y-%m-%dT%H:%M:%S.%f")
   time_stamp_fmt      = time_stamp_datetime.strftime("%Y-%m-%d %H:%M:%S")

   last_record = [time_stamp_fmt, keg_id, val, lat, lon, rssi]
   return render_template('smart_keg_http.html', record = last_record)


@app.route("/track_db", methods=['POST'])
def use_http_integration():
   '''
   Saving the data pushed by the TTN http integration
   '''
   
   # getting the data
   data = request.get_json()

   # extracting the data (later can extract lat long as well and compute max RSSI)
   keg_id     = data['dev_id']
   val        = data['payload_fields']['val']
   time_stamp = data['metadata']['time']
   rssi       = data['metadata']['gateways'][0]['rssi']
   lat        = -34.4062924
   lon        = 150.8813907
   
   # dump into a file
   with open(json_path, 'w') as outfile:
   	json.dump(data, outfile)

   return("OK")
  
if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080)

