import os
import logging
import json
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class Site(db.Model):
    """
    Represent a CSA pick-up location
    """
    title = db.StringProperty()
    lat = db.FloatProperty()
    lng = db.FloatProperty()
    desc_short = db.StringProperty()
    desc_long = db.StringProperty()

class FindSites(webapp.RequestHandler):
	def get(self):
		nearestSites = {
			"foo" : "bar"
		}
		self.response.headers = {'Content-Type': 'application/json; charset=utf-8'}
		self.response.out.write(json.dumps(nearestSites))

class MainPage(webapp.RequestHandler):
    """
    Render the main landing page where users can view the map and details about CSAs.
    """
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication(
	[('/', MainPage),
	('/nearestSites', FindSites)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()