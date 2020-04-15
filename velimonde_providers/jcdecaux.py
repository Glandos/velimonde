# encoding: utf-8
#
# JCDecaux
# http://developer.jcdecaux.com/
#

# update options
#   api_key : JCDecaux API key (required)

import urllib.request, urllib.error, urllib.parse
import json
import sys

# cities = { 'local name' : {
#    'country'  : (2 letters ISO 3166)' }}
# the local name is the one displayed beside the map
# see http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2
cities = {
    'Amiens'             : { 'country': 'FR' } ,
    'Besancon'           : { 'country': 'FR' } ,
    'Bruxelles-Capitale' : { 'country': 'FR' } ,
    'Cergy-Pontoise'     : { 'country': 'FR' } ,
    'Créteil'            : { 'country': 'FR' } ,
    'Göteborg'           : { 'country': 'SE' } ,
    'Ljubljana'          : { 'country': 'SI' } ,
    'Luxembourg'         : { 'country': 'LU' } ,
    'Lyon'               : { 'country': 'FR' } ,
    'Marseille'          : { 'country': 'FR' } ,
    'Mulhouse'           : { 'country': 'FR' } ,
    'Namur'              : { 'country': 'BE' } ,
    'Nancy'              : { 'country': 'FR' } ,
    'Nantes'             : { 'country': 'FR' } ,
    'Paris'              : { 'country': 'FR' } ,
    'Rouen'              : { 'country': 'FR' } ,
    'Santander'          : { 'country': 'ES' } ,
    'Sevilla'            : { 'country': 'ES' } ,
    'Stockholm'          : { 'country': 'SE' } ,
    'Toulouse'           : { 'country': 'FR' } ,
    '富山市'             : { 'country': 'JP' } ,
    'Valencia'           : { 'country': 'ES' }
}

# Unused for now
info = {
    'provider' : 'JCDecaux',                               # name of the data provider
    'info_url' : '',                                       # where to get info (users) where applicable
    'dev_info_url' :  'http://developer.jcdecaux.com/' ,   # where to get more info (developers)
    'logo_filename' :  ''                                  # logo file which should be located under
                                                           # static/imgs/logos
}

_provider_ids = {
    'Amiens'             : 'Amiens',
    'Besancon'           : 'Besancon',
    'Bruxelles-Capitale' : 'Bruxelles-Capitale',
    'Cergy-Pontoise'     : 'Cergy-Pontoise',
    'Créteil'            : 'Creteil',
    'Göteborg'           : 'Goteborg',
    'Ljubljana'          : 'Ljubljana',
    'Luxembourg'         : 'Luxembourg',
    'Lyon'               : 'Lyon',
    'Marseille'          : 'Marseille',
    'Mulhouse'           : 'Mulhouse',
    'Namur'              : 'Namur',
    'Nancy'              : 'Nancy',
    'Nantes'             : 'Nantes',
    'Paris'              : 'Paris',
    'Rouen'              : 'Rouen',
    'Santander'          : 'Santander',
    'Sevilla'            : 'Seville',
    'Stockholm'          : 'Stockholm',
    'Toulouse'           : 'Toulouse',
    '富山市'             : 'Toyama',
    'Valencia'           : 'Valence'
}

def update(options={}):
    """Download the data for each cities, storing it in json format in data/<name>.json
    It should be an array of dicts, each with the following keys:
        id              : (int) the ID of the station, must be unique for the city
        name            : (string) the name of the station (usually tied to location)
        position        : (dict) a dict with 'lat' and 'lng' keys, the latitude and longitude, as floats
        open            : (bool) whether the station is available
        bike_stands     : (int) the total number of stands, or docks, available at this station
        available_bikes : (int) the number of bikes available at this station
        last_update     : (int) the unix time of the last data update, in msecs
    """
    api_key = options['api_key']
    if api_key:
        c_info_url_format = "https://api.jcdecaux.com/vls/v1/stations?contract={0}&apiKey="+api_key
        for k, v in cities.items():
            url = c_info_url_format.format(_provider_ids[k])
            try:
                r = urllib.request.urlopen(url)
                in_json  = json.load(r)
                out_json = _reformat_json(in_json, k)
                with open('data/{0}.json'.format(k), 'w') as f:
                    json.dump(out_json, f, separators=(',',':'));
            except:
                sys.stderr.write('Failed to retrieve data for {0} ({1} plugin)'.format(k, __name__))
    else:
        sys.stderr.write('JCDecaux API key not defined in options dict')

def _reformat_json(data, city):
    stations = []
    for s in data:
        try:
            position = { 'lat' : round(s['position']['lat'], 6), 'lng' : round(s['position']['lng'], 6) }
        except:
            if 'name' in s:
                sys.stderr.write('Coordinates for station "{0}" ({1}) could not be parsed, it will not show on the map\n'.format(s['name'], city))
            else:
                raise KeyError
            position = { 'lat' : 0, 'lng' : 0 }
        station = {
            'id'              : s['number'],
            'name'            : s['name'],
            'position'        : position,
            'open'            : s['status'] == 'OPEN',
            'bike_stands'     : s['bike_stands'],
            'available_bikes' : s['available_bikes'],
            'last_update'     : s['last_update']
        }
        stations.append(station)
    return stations

