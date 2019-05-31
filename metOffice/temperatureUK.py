from weather import *
import sys
import pprint

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