# Scrape Transport for London (TFL) website for status updates
# Export the status updates as a CSV file
# Partly based on https://www.youtube.com/watch?v=XQgXKtPSzUI&list=WL&index=365&t=0s

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup

# user agent string
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0'}

my_url = 'https://tfl.gov.uk/tube-dlr-overground/status/'

# opening connection, grabbing the page
req = Request(my_url, headers=headers) # https://medium.com/@speedforcerun/python-crawler-http-error-403-forbidden-1623ae9ba0f
uClient = urlopen(req)
page_html = uClient.read()
uClient.close() # https://www.programcreek.com/python/example/81250/urllib.request.read

# html parsing
page_soup = soup(page_html, "html.parser")

# grab each line
lines_details = page_soup.findAll("div",{"id": "rainbow-list-tube-dlr-overground-tflrail-tram"})

for line_details in lines_details:
	lines = line_details.findAll("li",{"class" : lambda L: L and L.startswith('rainbow-list-item')}) # https://stackoverflow.com/questions/14257717/python-beautifulsoup-wildcard-attribute-id-search

filename = 'tfl_status.csv'
f = open(filename, "w")

headers = "service_name,status\n"
f.write(headers)

for line in lines:
	service_name = line.findAll("span", {"class":"service-name"})
	line_name = service_name[0].contents[1].text
	
	summary = line.findAll("span", {"class":"disruption-summary"})
	line_status = summary[0].contents[1].text.strip()
	line_status = line_status.replace("\n","& ")
	print(line_name + ': ' + line_status)
	f.write(line_name + "," + line_status + "\n")
	
f.close()

