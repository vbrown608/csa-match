### Scrape CSA webpages to get all their sites!

import httplib2
from bs4 import BeautifulSoup, SoupStrainer
import re

http = httplib2.Http()
status, response = http.request('http://happychildcsa.csaware.com/store/csadetails.jsp')

soup = BeautifulSoup(response)
tables = map(lambda x: x.parent, soup.find_all("tr", "tableHead"))

def processTable(table):
	name = table.find("b").find(text=True).strip()

	details = table.find_all(class_="txt1_gb")
	time = details[0].next_sibling.find(text=True).strip().replace("\n", " ")
	if len(details) >= 2:
		address = details[1].next_sibling.find(text=True).strip().replace("\n", " ")
	else:
		address = 'No address'

	return (name, address, time)

csa_list = []
for table in tables:
	csa_list += [processTable(table)]


status, response = http.request('http://cw.csaware.com/store/dropsmap.jsp?id=3963')
regex = r"new Drop\((.*?)\)"
drops = re.findall(regex, response,  re.DOTALL)
print drops


	
