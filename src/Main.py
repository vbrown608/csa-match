import os
import logging
import json
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
import datetime
import time

class CSA(db.Model):
	name = db.StringProperty()
	desc = db.StringProperty()

	def to_dict(self):
		output = {}
		SIMPLE_TYPES = (int, long, float, bool, dict, basestring, list)

		for key, prop in self.properties().iteritems():
			value = getattr(self, key)

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
				output[key] = value.to_dict()
			else:
				raise ValueError('cannot encode ' + repr(prop))

		return output

class Site(db.Model):
	"""
	Represent a CSA pick-up location
	"""
	csa = db.ReferenceProperty(CSA)
	address = db.StringProperty()
	lat = db.FloatProperty()
	lng = db.FloatProperty()
	

	def to_dict(self):
		output = {}
		SIMPLE_TYPES = (int, long, float, bool, dict, basestring, list)

		for key, prop in self.properties().iteritems():
			value = getattr(self, key)

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
				output[key] = value.to_dict()
			else:
				raise ValueError('cannot encode ' + repr(prop))

		return output

class FindSites(webapp.RequestHandler):
	def get(self):
		nearestSites = db.GqlQuery("SELECT * FROM Site").fetch(30)
		info = map(lambda x: x.to_dict(), nearestSites)
		logging.info(info)
		self.response.headers = {'Content-Type': 'application/json; charset=utf-8'}
		self.response.out.write(json.dumps(info))

class MainPage(webapp.RequestHandler):
	"""
	Render the main landing page where users can view the map and details about CSAs.
	"""
	def get(self):
		# my_csa = CSA(name = 'Phat Beets Produce', desc = 'Phat Beets Produce is a food justice collective.')
		# my_csa.put()
		# my_site = Site(csa = my_csa, address = 'Delmer St. & Laguna Ave., Oakland', lat = 0.0, lng = 0.0)
		# my_site.put()

		nearestSites = db.GqlQuery("SELECT * FROM Site").fetch(30)
		site_list = map(lambda x: x.to_dict(), nearestSites)

		template_values = { 'site_list' : site_list }
		path = os.path.join(os.path.dirname(__file__), 'index.html')
		self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication(
	[('/', MainPage),
	('/nearestSites', FindSites)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()