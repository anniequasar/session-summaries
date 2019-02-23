#Author:Annie

import json

from urllib.request import urlopen

api_key = '4067...................97873'

contract_name = 'Brisbane'

url_station_list='https://api.jcdecaux.com/vls/v1/stations?contract={contract_name}&apiKey={api_key}'

response = urlopen(url_station_list.format(contract_name=contract_name, api_key=api_key))

station_list = json.load(response)

#print(json.dumps(station_list,indent=4,sort_keys=True))

mostbikes = 0

for station in station_list:
    if station['available_bikes'] > mostbikes:
        mostbikes = station["available_bikes"]
        moststation = station

#print(moststation)

print(json.dumps(moststation,indent=4,sort_keys=True))
