import csv
import logging
import os

from models import *
import config

from google.appengine.ext import ndb
from google.appengine.api import search

def clearAllData(sample_data=True):
  """
  Clear all CSAs and Sites from the datastore.
  Clear all documents from the search index.
  """
  logging.info('Clearing datastore')
  csa_keys = CSA.query().fetch(keys_only=True)
  result = ndb.delete_multi(csa_keys)

  site_keys = Site.query().fetch(keys_only=True)
  ndb.delete_multi(site_keys)

  logging.info('Clearing search index')
  doc_index = search.Index(name=config.SITE_INDEX_NAME)
  try:
    while True:
      # until no more documents, get a list of documents,
      # constraining the returned objects to contain only the doc ids,
      # extract the doc ids, and delete the docs.
      document_ids = [document.doc_id
                      for document in doc_index.get_range(ids_only=True)]
      if not document_ids:
        break
      doc_index.delete(document_ids)
  except search.Error:
    logging.exception("Error removing documents:")

def loadFromCSV():
  logging.info('Loading CSA data')
  datafile = os.path.join('data', config.CSA_DATA)
  reader = csv.DictReader(
      open(datafile, 'rU'),
      ['id', 'name', 'description'])

  for row in reader:
    csa = CSA(id = row['id'], name = row['name'], description = row['description'], url = 'foo')
    csa.put()

  logging.info('Loading Site data')
  datafile = os.path.join('data', config.SITE_DATA)
  reader = csv.DictReader(
      open(datafile, 'rU'),
      ['csa', 'name', 'address', 'lat', 'lng'])

  for row in reader:
    csa_key = ndb.Key(CSA, row['csa'])
    site = Site(csa = csa_key, name=row['name'], address = row['address'], lat = float(row['lat']), lng = float(row['lng']))
    site.put()


