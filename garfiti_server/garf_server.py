from google.appengine.ext import db
from google.appengine.ext import webapp
from django.utils import simplejson
import rest

# skipping the image for now

class GarfModel(db.Model):
  to = db.StringProperty(indexed=True)
  from_who = db.StringProperty(indexed=True)
  title = db.StringProperty(indexed=False)
  hidden_message = db.StringProperty(indexed=False)
  date = db.DateTimeProperty(auto_now_add=True)

# add a handler for "rest" calls
application = webapp.WSGIApplication([
  ('/rest/.*', rest.Dispatcher)
], debug=True)

# configure the rest dispatcher to know what prefix to expect on request urls
rest.Dispatcher.base_url = "/rest"

rest.Dispatcher.model_handlers = {}
rest.Dispatcher.add_models({
  "garf": GarfModel})

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
