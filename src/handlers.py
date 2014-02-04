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
		#nearestSites = ndb.GqlQuery("SELECT * FROM Site").fetch(30)
		#info = map(lambda x: self.to_dictionary(x), nearestSites)
		info = {}
		logging.info(info)
		self.render_json(info)

class IndexHandler(BaseHandler):
	"""
	Render the main landing page where users can view the map and details about CSAs.
	"""
	def get(self):
		my_csa = CSA(name = 'Phat Beets Produce', desc = 'Phat Beets Produce is a food justice collective.')
		my_csa.put()
		my_site = Site(csa = my_csa.key, address = 'Delmer St. & Laguna Ave., Oakland', lat = 50.0, lng = 50.0)
		my_site.put()

		#nearestSites = ndb.GqlQuery("SELECT * FROM Site").fetch(30)
		#site_list = map(lambda x: self.to_dictionary(x), nearestSites)
		site_list = {}
		template_values = { 'site_list' : site_list }
		self.render_template('index.html', template_values)




