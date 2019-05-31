#! python3
# Get the current temperature in a location in the UK using Met Office API

from config import MET_OFFICE_API_KEY
import requests
import sys
import pprint
from datetime import datetime

TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

def request_met_office(resource, params = ''):
  if len(params) > 0:
    params += '&'
  params += 'key=' + MET_OFFICE_API_KEY
  url = 'http://datapoint.metoffice.gov.uk/public/data/' + resource + '?' + params
  response = requests.get(url)
  response.raise_for_status()
  return response.json()

def getLocationID(api_key, desired_location = 'London'):
  locations = request_met_office('val/wxfcs/all/json/sitelist') # daily and three-hourly forecast
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
  capabilities = request_met_office('val/wxfcs/all/json/capabilities', params = 'res=3hourly')
  timestamps = capabilities['Resource']['TimeSteps']['TS'] # a list of timestamps
  current_timestamp = datetime.today()

  deltas = []
  for timestamp in timestamps:
    timestamp_datetime = datetime.strptime(timestamp, TIME_FORMAT)
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
weather = request_met_office('val/wxfcs/all/json/' + location_id, params = 'res=3hourly&time=' + current_timestamp) # JSON to Python dict

rep = weather['SiteRep']['DV']['Location']['Period']['Rep']
#pprint.pprint(rep)

temperature = rep['T']

print('Temperature in ' + location_name + ': ' + str(temperature) + ' degrees C')