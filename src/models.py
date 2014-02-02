import logging

#import categories
#import docs

import datetime
from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import db	

class CSA(db.Model):
	name = db.StringProperty()
	desc = db.StringProperty()

class Site(db.Model):
	"""
	Represent a CSA pick-up location
	"""
	csa = db.ReferenceProperty(CSA)
	address = db.StringProperty()
	lat = db.FloatProperty()
	lng = db.FloatProperty()