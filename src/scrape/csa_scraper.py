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

class Scraper():
	def __init__(self, csa):
		self.csa = csa

	def scrape(self, url):
		soup = self.loadSoup(url)
		sites = self.sitesFromHTML(soup)
		return sites

	def loadSoup(self, url):
		http = httplib2.Http()
		status, response = http.request('http://happychildcsa.csaware.com/store/csadetails.jsp')
		return BeautifulSoup(response)

	def sitesFromHTML(self, soup):
		tables = map(lambda x: x.parent, soup.find_all("tr", "tableHead"))
		result = []
		for table in tables:
			result += [self.siteFromTable(table)]
		return result

	def siteFromTable(self, table):
		result = Site(self.csa)

		result.name = table.find("b").find(text=True).strip()
		details = table.find_all(class_="txt1_gb")
		result.time = details[0].next_sibling.find(text=True).strip().replace("\n", " ")
		if len(details) >= 2:
			result.address = details[1].next_sibling.find(text=True).strip().replace("\n", " ")

		return result

	def getLatLng(self, url, sites):
		status, response = http.request(url)
		regex = r"new Drop\((.*?)\)"
		triples = map(ast.literal_eval, re.findall(regex, response,  re.DOTALL))
		locations = dict(map(lambda x: (x[0], (x[1], x[2])), triples)) # Convert to a dictionary

		for site in sites:
			if site.name and site.name in locations:
				site.lat, site.lng = locations[site.name]

	def toCSV(self, sites):
		with open("sites.csv", "wb") as csvfile:
			siteWriter = csv.writer(csvfile, delimiter=',')
			for site in sites:
				siteWriter.writerow([site.csa, site.name, site.address, site.lat, site.lng])


#happychild = Scraper('Happy Child CSA')
#result = happychild.scrape('http://happychildcsa.csaware.com/store/csadetails.jsp')
#drops = happychild.getLatLng('http://cw.csaware.com/store/dropsmap.jsp?id=3963', result)
#happychild.toCSV(result)


# Classes
	# CSA with toCSV function
	# Scraper base class - individual scrapers inherit from this\
		# Geocode method
