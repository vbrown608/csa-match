from handlers import *
import webapp2
import logging

application = webapp2.WSGIApplication(
	[('/', IndexHandler),
	 ('/nearestSites', FindSites)
	], 
	debug=True)

def main():
    application.run()

if __name__=='__main__':
    main()