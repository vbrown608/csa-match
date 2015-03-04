### Scrape CSA webpages to get all their sites!

import httplib2
from bs4 import BeautifulSoup, SoupStrainer
import re
import csv
import ast #used to evaluate string representation of list

class Site():
	def __init__(self, csa = None, name = None, address = None, time = None, lat = None, lng = None):
		self.csa = csa
		self.name = name
		self.address = address
		self.time = time
		self.lat = lat
		self.lng = lng

def scrape(url, csa): 
	http = httplib2.Http()
	status, response = http.request(url)
	soup = BeautifulSoup(response)
	sites = sites_from_HTML(soup, csa)
	return sites

def sites_from_HTML(soup, csa):
	tables = map(lambda x: x.parent, soup.find_all("tr", "tableHead"))
	result = []
	for table in tables:
		result += [parse_site(table, csa)]
	return result

def parse_site(table, csa):
	result = Site(csa)
	result.name = table.find("b").find(text=True).strip()
	details = table.find_all(class_="txt1_gb")
	result.time = details[0].next_sibling.find(text=True).strip().replace("\n", " ")
	if len(details) >= 2:
		result.address = details[1].next_sibling.find(text=True).strip().replace("\n", " ")
	return result

def getLatLng(url, sites):
	http = httplib2.Http()
	status, response = http.request(url)
	regex = r"new Drop\((.*?)\),"
	triples = map(ast.literal_eval, re.findall(regex, response,  re.DOTALL))
	locations = dict(map(lambda x: (x[0], (x[1], x[2])), triples)) # Convert to a dictionary

	for site in sites:
		if site.name and site.name in locations:
			site.lat, site.lng = locations[site.name]
	return sites

def to_CSV(sites):
	with open("sites.csv", "a") as csvfile:
		siteWriter = csv.writer(csvfile, delimiter=',')
		for site in sites:
			siteWriter.writerow([site.csa, site.name, site.lat or 0, site.lng or 0, site.time, site.address])


#clear CSV
filename = 'sites.csv'
f = open(filename, "w+")
f.close()

happychild = scrape('http://happychildcsa.csaware.com/store/csadetails.jsp', 'happychild')
happychild = getLatLng('http://cw.csaware.com/store/dropsmap.jsp?id=3963', happychild)
to_CSV(happychild)

shootingstar = scrape('http://shootingstar.csaware.com/store/csadetails.jsp', 'shootingstar')
shootingstar = getLatLng('http://cw.csaware.com/store/dropsmap.jsp?id=15', shootingstar)
to_CSV(shootingstar)

marinsun = scrape('http://marinsunfarms.csaware.com/store/csadetails.jsp', 'marinsun')
marinsun = getLatLng('http://cw.csaware.com/store/dropsmap.jsp?id=4634', marinsun)
to_CSV(marinsun)
