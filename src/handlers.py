import logging
import time
import traceback
import urllib
import wsgiref

from base_handler import BaseHandler
#import config
#import docs
from models import *
import load_data
import json
import find_site
#import utils

from google.appengine.api import search
from google.appengine.api import users
from google.appengine.ext.deferred import defer
from google.appengine.ext import ndb	

class UpdateDataHandler(BaseHandler):
	"""
	Update the CSAs in the datastore based on CSV data
	"""
	def get(self):
		load_data.clearAllData()
		load_data.loadFromCSV()

class GetPinsHandler(BaseHandler):
	"""
	Return a list of sites near a given coordinate set
	"""
	def get(self):
		lat = self.request.get('lat') or 37.85
		lat = float(lat)
		lng = self.request.get('lng') or -122.25
		lng = float(lng)

		# Search for the nearest sites
		query = find_site.buildQuery(lat, lng, 1000, 1000000)
		nearby_sites = find_site.runSearch(query)

		self.render_json(nearby_sites)

class CSAHandler(BaseHandler):
	"""
	Get the description of a CSA
	"""
	def get(self, csa_id):
		csa = CSA.get_by_id(csa_id)
		self.render_template('_csa.html', csa.to_dict())

class IndexHandler(BaseHandler):
	"""
	Render the main landing page where users can view the map and details about CSAs.
	"""
	def get(self):
		address = self.request.get('address') or 'Address'
		lat = self.request.get('lat') or 37.85
		lat = float(lat)
		lng = self.request.get('lng') or -122.25
		lng = float(lng)
		zoom = 13 if self.request.get('address') else 10

		# Search for the nearest sites
		query = find_site.buildQuery(lat, lng, limit=6)
		nearby_sites = find_site.runSearch(query)
		logging.info(nearby_sites[0])

		template_values = { 'site_list' : nearby_sites,
												'pins' : json.dumps(nearby_sites),
												'lat' : lat,
												'lng' : lng,
												'address' : address, 
												'zoom' : zoom}
		self.render_template('index.html', template_values)


