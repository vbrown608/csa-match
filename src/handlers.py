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
from google.appengine.ext import db	
# from google.appengine.ext import webapp

def toDictionary(model):
	output = {}
	SIMPLE_TYPES = (int, long, float, bool, dict, basestring, list)

	for key, prop in model.properties().iteritems():
		value = getattr(model, key)

		if value is None or isinstance(value, SIMPLE_TYPES):
			output[key] = value
		elif isinstance(value, datetime.date):
			# Convert date/datetime to MILLISECONDS-since-epoch (JS "new Date()").
			ms = time.mktime(value.utctimetuple()) * 1000
			ms += getattr(value, 'microseconds', 0) / 1000
			output[key] = int(ms)
		elif isinstance(value, db.GeoPt):
			output[key] = {'lat': value.lat, 'lon': value.lon}
		elif isinstance(value, db.Model):
			output[key] = toDictionary(value)
		else:
			raise ValueError('cannot encode ' + repr(prop))

	return output

class FindSites(BaseHandler):
	def get(self):
		nearestSites = db.GqlQuery("SELECT * FROM Site").fetch(30)
		info = map(lambda x: toDictionary(x), nearestSites)
		logging.info(info)
		#self.response.headers = {'Content-Type': 'application/json; charset=utf-8'}
		#self.response.out.write(json.dumps(info))
		self.render_json(info)

class MainPage(BaseHandler):
	"""
	Render the main landing page where users can view the map and details about CSAs.
	"""
	def get(self):
		# my_csa = CSA(name = 'Phat Beets Produce', desc = 'Phat Beets Produce is a food justice collective.')
		# my_csa.put()
		# my_site = Site(csa = my_csa, address = 'Delmer St. & Laguna Ave., Oakland', lat = 0.0, lng = 0.0)
		#my_site.put()
		nearestSites = db.GqlQuery("SELECT * FROM Site").fetch(30)
		site_list = map(lambda x: toDictionary(x), nearestSites)

		template_values = { 'site_list' : site_list }
		#path = os.path.join(os.path.dirname(__file__), 'index.html')
		self.render_template('index.html', template_values)