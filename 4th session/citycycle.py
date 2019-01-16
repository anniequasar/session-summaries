# See https://data.brisbane.qld.gov.au for other data sets

# Register at https://developer.jcdecaux.com/ to get an api_key

# contract list GET https://api.jcdecaux.com/vls/v1/contracts?apiKey={api_key} HTTP/1.1

# station list  GET https://api.jcdecaux.com/vls/v1/stations?contract={contract_name}&apiKey={api_key} HTTP/1.1

# station info  GET https://api.jcdecaux.com/vls/v1/stations/{station_number}?contract={contract_name}&apiKey={api_key} HTTP/1.1



from urllib.request import urlopen

import json



# TODO enter your api key as issued by jcdecaux

api_key = '1fbb..............................82151e'

# contract name from jcdecaux contract list

contract_name = 'Brisbane'

# url for station list with placeholders for contract name and api key

url_station_list = "https://api.jcdecaux.com/vls/v1/stations?contract={contract_name}&apiKey={api_key}"

# use str format function to replace placeholders with values from variables

url = url_station_list.format(contract_name=contract_name, api_key=api_key)

# load the json (JavaScript Object Notation) data from the url's http response into a python list of dicts

station_list = json.load(urlopen(url))

# initialise variables which will capture the bike stations with the most available bikes

stations_with_most_bikes = []

most_bikes = 0

# Loop through all bike stations finding those with the maximum number of available bikes (could be more than one)

for station in station_list:

    print(station)

    if most_bikes < station['available_bikes']:

        # This station exceeds all previous ones so replace list with just this one and save the number of bikes

        most_bikes = station['available_bikes']

        stations_with_most_bikes = [station]

    elif most_bikes == station['available_bikes']:

        # This station equals previous maximum so add it to the list

        stations_with_most_bikes.append(station)

# Display results

print()

print("Most number of available bikes =", most_bikes, 'at the following station(s)')

for station in stations_with_most_bikes:

    print(station['name'], 'at', station['position'])
