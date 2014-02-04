import logging
import time
import traceback
import urllib
import wsgiref

from base_handler import BaseHandler
#import config
#import docs
from models import *
#import utils

from google.appengine.api import search
from google.appengine.api import users
from google.appengine.ext.deferred import defer
from google.appengine.ext import ndb	

class FindSites(BaseHandler):
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
				site_info = model.to_dictionary()
				nearby_sites += [site_info]
		except search.Error:
		    logging.exception('Search failed')
		self.render_json(nearby_sites)

class IndexHandler(BaseHandler):
	"""
	Render the main landing page where users can view the map and details about CSAs.
	"""
	def get(self):
		# my_csa = CSA(name = 'Phat Beets Produce', desc = 'Phat Beets Produce is a food justice collective.')
		# my_csa.put()
		# my_site = Site(csa = my_csa.key, address = 'Delmer St. & Laguna Ave., Oakland', lat = 50.0, lng = 50.0)
		# my_site.put()

		index = search.Index(name=config.SITE_INDEX_NAME)
		query_string = 'distance(location, geopoint(50.0, 50.0)) < 20'
		nearby_sites = []

		try:
		    results = index.search(query_string) 
		    # Iterate over the documents in the results
		    for r in results:
		    	site_id = int(r['id'][0].value)
		    	model = Site.get_by_id(site_id)

		    	site_info = model.to_dictionary()
		    	nearby_sites += [site_info]
		except search.Error:
		    logging.exception('Search failed')

		template_values = { 'site_list' : nearby_sites }
		self.render_template('index.html', template_values)




