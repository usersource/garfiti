from google.appengine.ext import db
from google.appengine.ext import webapp
import rest

# skipping the image for now

class GarfModel(db.Model):
    garf_to = db.StringProperty(indexed=True)
    garf_from = db.StringProperty(indexed=True)
    garf_title = db.StringProperty(indexed=False)
    garf_hidden_message = db.StringProperty(indexed=False)
    date = db.DateTimeProperty(auto_now_add=True)

grf = GarfModel()

grf.garf_to = "ABC"
grf.garf_from = "JKL"
grf.garf_title = "123"
grf.garf_hidden_message = "456"
        
sys.stdout.write(grf.to_xml())


