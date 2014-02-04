import models

from google.appengine.api import search
from google.appengine.ext import ndb

import collections
import copy
import datetime
import logging
import re
import string

import config

class CSA():
  _INDEX_NAME = config.CSA_INDEX_NAME

class Site():
  _INDEX_NAME = config.SITE_INDEX_NAME

  CSA = 'csa'
  ADDRESS = 'address'
  LAT = 'lat'
  LNG = 'lng'