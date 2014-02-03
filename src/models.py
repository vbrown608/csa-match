import logging

#import categories
#import docs

import datetime
from google.appengine.api import memcache
from google.appengine.ext import ndb	

class CSA(ndb.Model):
	name = ndb.StringProperty()
	desc = ndb.StringProperty()

class Site(ndb.Model):
	"""
	Represent a CSA pick-up location
	"""
	csa = ndb.KeyProperty(kind=CSA)
	address = ndb.StringProperty()
	lat = ndb.FloatProperty()
	lng = ndb.FloatProperty()