# Scrape BBC weather page 
# Print a London weather summary for today and tomorrow
# Partly based on https://www.youtube.com/watch?v=XQgXKtPSzUI&list=WL&index=365&t=0s

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup

location = '2643743' # London

# user agent string
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0'}

my_url = 'https://www.bbc.co.uk/weather/' + location

# opening connection, grabbing the page
req = Request(my_url, headers=headers) # https://medium.com/@speedforcerun/python-crawler-http-error-403-forbidden-1623ae9ba0f
uClient = urlopen(req)
page_html = uClient.read()
uClient.close() # https://www.programcreek.com/python/example/81250/urllib.request.read

# html parsing
page_soup = soup(page_html, "html.parser")

# ------- TODAY ----------------------------------------------

today = page_soup.findAll("a",{"href": "/weather/" + location + "/today"})

# max/min temperature

temperature_class_today = today[0].findAll("span",{"class" : "wr-value--temperature--c"})
temperature_highest_today = temperature_class_today[0].contents[0]

print("The highest/lowest temperature in London today/tonight: " + temperature_highest_today + "C") 

# weather summary

summary_today_class = today[0].findAll("div", {"class" : "wr-day__details__weather-type-description"})
summary_today = summary_today_class[0].contents[0]

print("Weather summary for today: " + summary_today)

# current temperature & next rain

carousel_today = page_soup.findAll("div",{"class" : "wr-time-slot-list wr-time-slot-list--day-0 wr-js-time-slot-list"})
temperatures = carousel_today[0].findAll("span",{"class" : "wr-value--temperature--c"})
temperature_now = temperatures[0].contents[0]

print("Current temperature: " + temperature_now)

cloud_types_dirty = carousel_today[0].findAll("div",{"class":"wr-weather-type__icon"})

cloud_types = []
for time_slot in range(len(cloud_types_dirty)):
	cloud_types.append(cloud_types_dirty[time_slot].get_text())
	
def next_rain():
	# find the time until it rain next
	for time_slot in range(len(cloud_types)):
		if "Rain" in cloud_types[time_slot]:
			return time_slot
	return float('Inf')
			
hours_until_rain = next_rain()
		
if hours_until_rain < float('Inf'):
	print("It may start raining in " + str(hours_until_rain) + "-" + str(hours_until_rain+1) + " hours")
elif hours_until_rain == float('Inf'):
	print("No rain in the next", len(cloud_types)-1 , "hours")

# sunset

sun_times = page_soup.findAll("span", {"class":"wr-c-astro-data__time"})
sunset_today = sun_times[1].text

print("Sunset: " + sunset_today)

# ------- TOMORROW -------------------------------------------

tomorrow = page_soup.findAll("a",{"href": "/weather/" + location + "/day1"})

# max/min temperature

temperature_class_tomorrow = tomorrow[0].findAll("span",{"class" : "wr-value--temperature--c"})
temperature_highest_tomorrow = temperature_class_tomorrow[0].contents[0]

print("The highest temperature in London tomorrow: " + temperature_highest_tomorrow + "C")

# weather summary

summary_tomorrow_class = tomorrow[0].findAll("div", {"class" : "wr-day__details__weather-type-description"})
summary_tomorrow = summary_tomorrow_class[0].contents[0]

print("Weather summary for tomorrow: " + summary_tomorrow)

