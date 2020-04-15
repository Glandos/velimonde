# encoding: utf-8
#
# Smovengo
# https://www.velib-metropole.fr/donnees-open-data-gbfs-du-service-velib-metropole
#

# update options

import urllib.request, urllib.error, urllib.parse
import json
import sys
import os
import datetime

cities = { 'Paris'             : { 'country': 'FR' } }

#Unused for now
info = {
    'provider' : 'Smovengo Paris',                         # name of the data provider
    'info_url' : '',                                       # where to get info (users) where applicable
    'dev_info_url' :  'https://www.velib-metropole.fr/donnees-open-data-gbfs-du-service-velib-metropole' ,   # where to get more info (developers)
    'logo_filename' :  ''                                  # logo file which should be located under
                                                           # static/imgs/logos
}

def update(options={}):
    status_url = 'https://velib-metropole-opendata.smoove.pro/opendata/Velib_Metropole/station_status.json'
    information_url = 'https://velib-metropole-opendata.smoove.pro/opendata/Velib_Metropole/station_information.json'
    try:
        status_json  = json.load(urllib.request.urlopen(status_url))
        information_json  = json.load(urllib.request.urlopen(information_url))
        out_json = _reformat_json(status_json, information_json)
        with open('data/Paris.json', 'w') as f:
            json.dump(out_json, f, separators=(',',':'));
    except:
        raise
        sys.stderr.write('Failed to retrieve data for Paris')

def _reformat_json(status, information):

    information = {s['station_id']: s for s in information['data']['stations']}

    stations = []
    for s in status['data']['stations']:
        s_info = information[s['station_id']]
        station = {
            'id'              : int(s['stationCode']),
            'name'            : s_info['name'],
            'position'        : {
                'lat': round(float(s_info['lat']), 6),
                'lng': round(float(s_info['lon']), 6)
                },
            'open'            : s['is_renting'] == 1,
            'bike_stands'     : s['num_docks_available'],
            'available_bikes' : s['num_bikes_available'],
            'last_update'     : s['last_reported']
        }
        stations.append(station)
    return stations

