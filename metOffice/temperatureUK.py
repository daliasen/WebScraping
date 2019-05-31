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

def get_location_id(desired_location = 'London'):
  locations = request_met_office('val/wxfcs/all/json/sitelist') # daily and three-hourly forecast
  locations = locations['Locations']['Location']

  for location in locations:  
    if desired_location.lower() == location['name'].lower():
      location_name = location['name']
      location_id = location['id']
  if 'location_name' not in locals():
    sys.exit('location ID not found')
  return location_id, location_name
  
def get_closest_timestamp():
  # find the timestamp closest to the current time
  capabilities = request_met_office('val/wxfcs/all/json/capabilities', params = 'res=3hourly')
  timestamps = capabilities['Resource']['TimeSteps']['TS'] # a list of timestamps
  current_timestamp = datetime.now()

  deltas = []
  for timestamp in timestamps:
    timestamp_datetime = datetime.strptime(timestamp, TIME_FORMAT)
    delta = current_timestamp - timestamp_datetime
    deltas.append(abs(delta.total_seconds()))
      
  closest_stamp = timestamps[deltas.index(min(deltas))]
  print('Closest timestamp: ' + str(closest_stamp))
  
  return closest_stamp

# Get the location from the command line arguments if specified
if len(sys.argv) > 1:
  desired_location = ' '.join(sys.argv[1:])

if 'desired_location' in locals():
  location_id, location_name = get_location_id(desired_location)
else:
  location_id, location_name = get_location_id() # use default location

current_timestamp = get_closest_timestamp()

# Download the JSON data from metoffice.gov.uk API.
weather = request_met_office('val/wxfcs/all/json/' + location_id, params = 'res=3hourly&time=' + current_timestamp) # JSON to Python dict

rep = weather['SiteRep']['DV']['Location']['Period']['Rep']
#pprint.pprint(rep)

temperature = rep['T']

print('Temperature in ' + location_name + ': ' + str(temperature) + ' degrees C')