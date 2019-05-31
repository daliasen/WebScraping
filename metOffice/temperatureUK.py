#! python3
# Get the current temperature in a location in the UK using Met Office API

import requests
import sys
import pprint
from datetime import datetime

def getLocationID(api_key, desired_location = 'London'):
  # find the location ID
  resource = 'val/wxfcs/all/json/sitelist' # locations with daily and three-hourly forecast
  url_location = 'http://datapoint.metoffice.gov.uk/public/data/%s?key=%s' % (resource, api_key)
  response_locations = requests.get(url_location)
  response_locations.raise_for_status()
  locations = response_locations.json() # JSON to Python dict
  locations = locations['Locations']['Location']

  for location in locations:  
    if desired_location.lower() == location['name'].lower():
      location_name = location['name']
      location_id = location['id']
  if 'location_name' not in locals():
    sys.exit('location ID not found')
  return location_id, location_name
  
def getCurrentTimestamp(api_key):
  # find the timestamp closest to the current time
  url_times = 'http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/capabilities?res=3hourly&key=%s' % (api_key)
  response_timestamps = requests.get(url_times)
  response_timestamps.raise_for_status()
  timestamps = response_timestamps.json() # JSON to Python dict

  timestamps = timestamps['Resource']['TimeSteps']['TS'] # a list of timestamps
  current_timestamp = datetime.today()

  deltas = []
  for timestamp in timestamps:
    timestamp_datetime = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
    delta = current_timestamp - timestamp_datetime
    deltas.append(abs(delta.total_seconds()))
    #print('timestamp: ' + str(timestamp))
    #print('delta: ' + str(delta))
    #print('delta, seconds: ' + str(delta.total_seconds()))
    #print('delta, seconds type: ' + str(type(delta.total_seconds())))
      
  closest_stamp = timestamps[deltas.index(min(deltas))]
  #print('deltas min index: ' + str(deltas.index(min(deltas))))
  print('Closest timestamp: ' + str(closest_stamp))
  
  return closest_stamp

# Get the API key from the command line arguments
if len(sys.argv) < 2:
  print('Usage: temperatureUK.py api_key\n Optional: location (London by default)')
  sys.exit()
  
api_key = sys.argv[1]

if len(sys.argv) > 2:
  desired_location = ' '.join(sys.argv[2:])

if 'desired_location' in locals():
  location_id, location_name = getLocationID(api_key, desired_location)
else:
  location_id, location_name = getLocationID(api_key) # use default location

current_timestamp = getCurrentTimestamp(api_key)

# Download the JSON data from metoffice.gov.uk API.
url ='http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/%s?res=3hourly&key=%s&time=%s' % (location_id, api_key, current_timestamp)

response_weather = requests.get(url)
response_weather.raise_for_status()
weather = response_weather.json() # JSON to Python dict

rep = weather['SiteRep']['DV']['Location']['Period']['Rep']
#pprint.pprint(rep)

temperature = rep['T']

print('Temperature in ' + location_name + ': ' + str(temperature) + ' degrees C')