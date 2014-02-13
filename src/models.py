import logging

#import categories

import datetime
from google.appengine.api import memcache
from google.appengine.ext import ndb	

from google.appengine.api import search 
import config

class CSA(ndb.Model):
	"""
	Represent a CSA - will have multiple sites associated to it.
	"""
	name = ndb.StringProperty()
	desc = ndb.StringProperty()

	def sites(self):
		"""Retrieve all the sites associated with this CSA"""
		return [] # Need to write this.

class Site(ndb.Model):
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

