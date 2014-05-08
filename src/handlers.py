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
#import utils

from google.appengine.api import search
from google.appengine.api import users
from google.appengine.ext.deferred import defer
from google.appengine.ext import ndb	

class FindSites(BaseHandler):
	"""
	Return a list of sites near a given coordinate set
	"""
	def get(self):
		index = search.Index(name=config.SITE_INDEX_NAME)
		query_string = 'distance(location, geopoint(50.0, 50.0)) < 100'
		nearby_sites = []

		try:
		    results = index.search(query_string) 
		    # Iterate over the documents in the results
		    for r in results:
				site_id = int(r['id'][0].value)
				model = Site.get_by_id(site_id)
				if model != None:
					site_info = model.to_dict()
					nearby_sites += [site_info]
				else:
					logging.exception('Could not retrieve model')
		except search.Error:
		    logging.exception('Search failed')
		#self.render_json(nearby_sites)

class IndexHandler(BaseHandler):
	"""
	Render the main landing page where users can view the map and details about CSAs.
	"""
	def get(self):
		address = self.request.get('address') or 'Address'
		lat = self.request.get('lat') or 37.85
		lng = self.request.get('lng') or -122.25

		index = search.Index(name=config.SITE_INDEX_NAME)
		query_string = ('distance(location, geopoint(' + str(lat) +
										', ' + str(lng) +
										')) < 10000') # distance is in meters, lol
		nearby_sites = []

		try:
			results = index.search(query_string) 
			# Iterate over the documents in the results
			for r in results:
				site_id = int(r['id'][0].value)
				model = Site.get_by_id(site_id)
				if model != None:
					site_info = model.to_dict(exclude=['csa']) # CSA property is just a key
					site_info['csa'] = model.csa.get().to_dict()
					nearby_sites += [site_info]
				else:
					logging.exception('Could not retrieve model')
		except search.Error:
		    logging.exception('Search failed')

		template_values = { 'site_list' : nearby_sites,
												'pins' : json.dumps(nearby_sites),
												'lat' : lat,
												'lng' : lng,
												'address' : address }
		self.render_template('index.html', template_values)


