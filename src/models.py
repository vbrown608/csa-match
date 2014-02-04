import logging

#import categories

import datetime
from google.appengine.api import memcache
from google.appengine.ext import ndb	

from google.appengine.api import search 
import config

class BaseModel(ndb.Model):
	def to_dictionary(self):
	    output = {}
	    SIMPLE_TYPES = (int, long, float, bool, dict, basestring, list)

	    for key, prop in self._properties.iteritems():
	      value = getattr(self, key)

	      if value is None or isinstance(value, SIMPLE_TYPES):
	        output[key] = value
	      elif isinstance(value, datetime.date):
	        # Convert date/datetime to MILLISECONDS-since-epoch (JS "new Date()").
	        ms = time.mktime(value.utctimetuple()) * 1000
	        ms += getattr(value, 'microseconds', 0) / 1000
	        output[key] = int(ms)
	      elif isinstance(value, ndb.GeoPt):
	        output[key] = {'lat': value.lat, 'lon': value.lon}
	      elif isinstance(value, ndb.Model):
	        output[key] = value.to_dictionary()
	      elif isinstance(value, ndb.Key):
	        output[key] = str(value) #value.to_dictionary()
	      else:
	        raise ValueError('cannot encode ' + repr(prop))
	    return output

class CSA(BaseModel):
	"""
	Represent a CSA - will have multiple sites associated to it.
	"""
	doc_id = ndb.StringProperty()
	name = ndb.StringProperty()
	desc = ndb.StringProperty()

	def sites(self):
		"""Retrieve all the sites associated with this CSA"""
		return [] # Need to write this.

class Site(BaseModel):
	"""
	Represent a CSA pick-up location
	"""
	#doc_id = ndb.StringProperty()
	csa = ndb.KeyProperty(kind=CSA)
	address = ndb.StringProperty()
	lat = ndb.FloatProperty()
	lng = ndb.FloatProperty()

	def _post_put_hook(self, future):
		"""
		Save an associated document to the search index so we can search for sites by location
		"""
		my_document = search.Document(
		    # Setting the doc_id is optional. If omitted, the search service will create an identifier.
		    fields=[
		       search.AtomField(name='id', value=str(self.key.id())),
		       search.GeoField(name='location', value=search.GeoPoint(self.lat, self.lng))
		       ])
		search.Index(name=config.SITE_INDEX_NAME).put(my_document)