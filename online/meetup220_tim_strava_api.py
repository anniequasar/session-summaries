#!/usr/bin/env python3
r"""MeetUp 220 - Beginners' Python and Machine Learning - 20 Aug 2025 - Using Strava API to monitor running and cycling

Learning objectives:
- Using Python's requests library to communicate with a REST API
- Using an access token with Strava's REST API
- Refreshing an access token with Strava's REST API
- Collecting user data from Strava's REST API
- Using oauth to create a Strava token with larger scope
- Collecting activity data from Strava
- Plotting an activity on a map

It is recommended to have a strava account with some activities containing map data

Links:
- Meetup: <https://www.meetup.com/beginners-python-machine-learning/events/310495090/>
- YouTube: <https://youtu.be/UAPDR00e-2s>
- Colab: <https://colab.research.google.com/drive/1MGTukijZ45KeYparjYhj_sabB-xaQvWL>
- GitHub: <https://github.com/timcu/bpaml-sessions/blob/master/online/meetup220_tim_strava_api.py>

References:
- Strava: https://strava.com (can create account using Google account)
- Strava developers: https://developers.strava.com (use same account)

@author D Tim Cummings

INSTALL THIRD PARTY LIBRARIES

```bash
pip install requests polyline folium
```

### Note from Strava about using their API

The Strava REST API includes data on athletes, segments, routes, clubs, and gear. It is free to use. The Strava API does not allow you to get data for all Strava public athletes, as you can see on our website.

To get data on athletes, you will have to make an application and request that athletes sign in with Strava, and grant your application certain permissions using OAuth 2.0. You can get data on yourself without authentication for testing purposes.

Strava API usage is limited on a per-application basis using both a 15-minute and daily request limit. The default rate limit allows 200 requests every 15 minutes, with up to 2,000 requests per day.

Go to <https://www.strava.com/settings/api> to create an API key,

 - Application name: bpaml
 - Category: DataImporter
 - Website: https://bpaml.pythonator.com
 - Description: Teaching python programming using an API such as Strava's
 - Authorized Callback Domain: developers.strava.com
"""
# Standard libraries
from pathlib import Path
from pprint import pprint as pp
import datetime
import json
import sys
import webbrowser
import zoneinfo
# Third party libraries
import folium
import polyline
import requests


print("Python version and executable", sys.version, sys.executable)

# This is how to create a file containing api keys
api_key_init = {
    "client_id": "my id",
    "client_secret": "my secret",
    "access_token": "my access token",
    "refresh_token": "my refresh token",
    "expires_at": int(datetime.datetime.now(datetime.timezone.utc).timestamp())
}
# Use python's pathlib for object oriented access to the file system
file_path = Path("json-demo.json")
# Create the directory to store the file if it doesn't exist
file_path.parent.mkdir(parents=True, exist_ok=True)
# Store dict in json format in file called "drive/MyDrive/api-keys/json-demo.json"
with file_path.open("w") as json_file:
    json.dump(api_key_init, json_file, indent=2)
# Read file back into a new variable to ensure it was written correctly
with file_path.open("r") as json_file:
    dummy_api_key = json.load(json_file)
pp(dummy_api_key)

# Task 1. Save your own API key to "strava-key.json"

# define a function which can display some api details but not all
def partial_reveal(dct_api_key: dict[str, str|int]):
    for k, v in dct_api_key.items():
        if isinstance(v, str):
            # Only show half of details to not give away secrets
            print(f"{k:13} = {v[:len(v)//2]}... full length={len(v)}")
        else:
            print(f"{k:13} = {v}")

# I am only going to read the file so as not to publicise my api key
file_path = Path("strava-key.json")
try:
    with file_path.open("r") as json_file:
        api_key = json.load(json_file)
except FileNotFoundError:
    sys.exit("strava-key.json not found. Please create manually in the same directory as this script.")
partial_reveal(api_key)

# define a function which refreshes access_token if it has expired
def refreshed_key(dct_api_key: dict[str, str|int]) -> dict[str, str|int]:
    """Refreshes api key if it has expired,

    stores new key in api-keys/strava.json
    returns new key as dict

    If api key has not expired, or refresh unsuccessful, returns the original key"""
    now = datetime.datetime.now(datetime.timezone.utc).timestamp()
    if "expires_at" not in dct_api_key or dct_api_key["expires_at"]<=now:
        print(f"Access token expired {dct_api_key.get('expires_at')=} {now=}")
        # https://developers.strava.com/docs/authentication/ "Refreshing Expired Access Tokens"
        my_token_url = 'https://www.strava.com/api/v3/oauth/token'

        my_payload = {
            'client_id': dct_api_key["client_id"],
            'client_secret': dct_api_key["client_secret"],
            'grant_type': 'refresh_token',
            'refresh_token': dct_api_key["refresh_token"]
        }

        my_response = requests.post(my_token_url, data=my_payload)

        if my_response.status_code == 200:
            new_tokens = my_response.json()
            # Update the api_key dictionary with the new access and refresh tokens and expiry time
            dct_api_key['access_token'] = new_tokens['access_token']
            dct_api_key['refresh_token'] = new_tokens['refresh_token']
            dct_api_key['expires_at'] = new_tokens['expires_at']
            print("Token refreshed successfully.")
            partial_reveal(dct_api_key) # Show the updated keys (partially)
            # Save the refreshed key for a later session
            key_file_path = Path(f"strava-key.json")
            with key_file_path.open("w") as f:
                json.dump(dct_api_key, f, indent=2)
        else:
            print(f"Error refreshing token: {my_response.status_code} - {my_response.text}")
    return dct_api_key

# Before every request, check if api_key needs refreshing
api_key = refreshed_key(api_key)

# Define the endpoint and headers
url = 'https://www.strava.com/api/v3/athlete'
headers = {
    'Authorization': f'Bearer {api_key["access_token"]}'
}

# Make the GET request
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.ok:
    api_owner_data = response.json()
    print("Athlete Data for owner of API key:")
    pp(api_owner_data)
else:
    print(f"Error {response.status_code}: {response.text}")

# To get activity data about any athlete I need to authenticate. Colab is not running in a local web server so this process is a bit manual.
import urllib.parse

token_path = Path("strava-token.json")
if token_path.exists():
    with token_path.open("r") as json_file:
        activity_token = json.load(json_file)
else:
    client_id = api_key['client_id']  # from https://www.strava.com/settings/api
    redirect_uri = 'http://localhost'  # or any dummy URI; we’ll grab the code manually but this matches our api key setup
    scope = 'read,activity:read'  # we only need to read data

    auth_url = (
        f"https://www.strava.com/oauth/authorize?"
        f"client_id={client_id}&response_type=code&redirect_uri={urllib.parse.quote(redirect_uri)}"
        f"&approval_prompt=force&scope={urllib.parse.quote(scope)}"
    )

    print("Open this URL to authorise:")
    print(auth_url)

    # Exchange the code for an access token
    # If redirected url is http://localhost/?state=&code=9047da5fd2ec6d1234c259a90d14665e667013f5&scope=read,activity:read
    # then code is 9047da5fd2ec6d1234c259a90d14665e667013f5
    client_secret = api_key['client_secret']
    code = input("Paste the code from the URL: ")

    token_url = 'https://www.strava.com/oauth/token'

    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'grant_type': 'authorization_code'
    }

    response = requests.post(token_url, data=payload)

    if response.ok:
        activity_token = response.json()
        partial_reveal(activity_token)
        file_path = Path(f"strava-token.json")
        with file_path.open("w") as json_file:
            json.dump(activity_token, json_file, indent=2)
    else:
        sys.exit(f"Error {response.status_code}: {response.text}")

# define a function which refreshes access_token if it has expired
def refreshed_token(dct_api_key: dict[str, str|int], dct_token) -> dict[str, str|int]:
    """Refreshes token if it has expired,

    stores new token in api-keys/strava-token.json
    returns new token as dict

    If token has not expired, or refresh unsuccessful, returns the original token"""
    now = datetime.datetime.now(datetime.timezone.utc).timestamp()
    if "expires_at" not in dct_token or dct_token["expires_at"]<=now:
        print(f"token expired {dct_token.get('expires_at')=} {now=}")
        # https://developers.strava.com/docs/authentication/ "Refreshing Expired Access Tokens"
        my_token_url = 'https://www.strava.com/api/v3/oauth/token'

        my_payload = {
            'client_id': dct_api_key["client_id"],
            'client_secret': dct_api_key["client_secret"],
            'grant_type': 'refresh_token',
            'refresh_token': dct_token["refresh_token"]
        }

        my_response = requests.post(my_token_url, data=my_payload)

        if my_response.status_code == 200:
            new_tokens = my_response.json()
            # Update the api_key dictionary with the new access and refresh tokens and expiry time
            dct_token['access_token'] = new_tokens['access_token']
            dct_token['refresh_token'] = new_tokens['refresh_token']
            dct_token['expires_at'] = new_tokens['expires_at']
            print("Token refreshed successfully.")
            partial_reveal(dct_token) # Show the updated keys (partially)
            # Save the refreshed key for a later session
            token_file_path = Path(f"strava-token.json")
            with token_file_path.open("w") as f:
                json.dump(dct_token, f, indent=2)
        else:
            print(f"Error refreshing token: {my_response.status_code} - {my_response.text}")
    return dct_token

"""### Use the swagger playground to explore the API

<https://developers.strava.com/playground/>

For example to get a list of athletes activities

`[GET] /athlete/activities`

- before (JavaScript epoch timestamp)
- after (JavaScript epoch timestamp)
- page (int default=1)
- per_page (int default=30)
"""

# How to create an integers matching a JavaScript epoch timestamp
# Timestamps are in seconds since 1-Jan-1970 00:00 UTC
# expires_at is epoch timestamp in seconds
# before and after are epoch timestamps in seconds

# I want all activities between 15-Dec-2024 and 1-Feb-2025

after = int(datetime.datetime(2024,12,15,0,0, tzinfo=zoneinfo.ZoneInfo("Australia/Brisbane")).timestamp())
before = int(datetime.datetime(2025,2,1,0,0, tzinfo=zoneinfo.ZoneInfo("Australia/Brisbane")).timestamp())

print(f"JavaScript epoch timestamps: {after} to {before}")

# Before every request, check if token needs refreshing
activity_token = refreshed_token(api_key, activity_token)

# Define the endpoint and headers
url = 'https://www.strava.com/api/v3/athlete/activities'
headers = {'Authorization': f'Bearer {activity_token["access_token"]}'}

# Define parameters for the request
params = {
    'before': before,
    'after':  after
}

# Make the GET request with parameters
response = requests.get(url, headers=headers, params=params)

# Check if the request was successful
if response.ok:
    activity_data = response.json()
    if activity_data:
        print("Athlete activities for authorized user:")
        for activity in activity_data:
            print(activity)
else:
    sys.exit(f"Error {response.status_code}: {response.text}")

for activity_item in activity_data[::-1]:
    start_time = datetime.datetime.strptime(activity_item["start_date"], "%Y-%m-%dT%H:%M:%SZ").astimezone(zoneinfo.ZoneInfo("Australia/Brisbane"))
    print(f'{start_time:%d-%b-%Y %H:%M} {activity_item["distance"] / 1000:6.1f}km {activity_item["name"]}')

# We can plot the course run, but we need to install some additional third party libraries into colab
# !pip install polyline folium

def plot_activity(lst_activity_data, name):
    """Assuming lst_activity_data is a list of activity dictionaries as retrieved from the Strava API"""
    if lst_activity_data:
        # Take the activity which is titled "Australia" and its polyline as an example
        for activity in lst_activity_data:
            if activity['name'].startswith(name):
                break
        else:
            return
        summary_polyline = activity.get('map', {}).get('summary_polyline')

        if summary_polyline:
            # Decode the polyline
            decoded_coords = polyline.decode(summary_polyline)
            # Create a map centered around the center of the polyline
            if decoded_coords:
                max_lat = max(decoded_coords, key=lambda x: x[0])[0]
                min_lat = min(decoded_coords, key=lambda x: x[0])[0]
                max_lon = max(decoded_coords, key=lambda x: x[1])[1]
                min_lon = min(decoded_coords, key=lambda x: x[1])[1]
                map_center = (max_lat + min_lat)/2, (max_lon + min_lon)/2

                m = folium.Map(location=[map_center[0], map_center[1]], zoom_start=16)

                # Add the polyline to the map
                folium.PolyLine(decoded_coords, color="blue", weight=2.5, opacity=1).add_to(m)

                # Display the map
                m.save(f"{name}.html")
                webbrowser.open(f"{name}.html")
            else:
                print("Could not decode the polyline.")
        else:
            print("No summary polyline found for the activity.")
    else:
        print("No activity data available to plot.")

plot_activity(activity_data, "Australia")
plot_activity(activity_data, "Face of St Lucia")
