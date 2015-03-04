import logging
import time
import traceback
import urllib
import wsgiref

from google.appengine.api import search
from google.appengine.ext import ndb	
from models import *

import config

def buildQuery(lat, lng, limit=10, distance=10000):
	limit = 1000 if limit > 1000 else limit
	query_string = ('distance(location, geopoint(%.3f, %.3f)) < %f' % (lat, lng, distance)) 
	sort1 = search.SortExpression(expression='distance(location, geopoint(%.3f, %.3f))' \
		% (lat, lng), 
		direction=search.SortExpression.ASCENDING, default_value=float('inf'))
	sort_opts = search.SortOptions(expressions=[sort1])
	query_options = search.QueryOptions(
		limit = limit,
		sort_options = sort_opts)
	query = search.Query(query_string=query_string, options=query_options) 
	return query

def runSearch(query):
	"""
	Take a query object, run the search, and process results
	"""
	index = search.Index(name=config.SITE_INDEX_NAME)
	nearby_sites = []
	try:
		results = index.search(query)
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
	return nearby_sites