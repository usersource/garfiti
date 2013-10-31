'''
Created on 30.10.2013
@author: Sergey Gadzhilov
'''

from google.appengine.ext import ndb
from garfiti_api_messages import GarfResponseMessage


class GarfModel(ndb.Model):
    
    to = ndb.StringProperty(indexed=True)
    from_who = ndb.StringProperty(indexed=True)
    title = ndb.StringProperty()
    message = ndb.StringProperty()
    image = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
           
    @classmethod
    def put_from_message(cls, request):
        entity = cls(to=request.to,
                     from_who=request.from_who,
                     title=request.title,
                     message=request.message,
                     image = request.image)
        entity.put()
        return entity.key.id()
    
    
    def to_response_message(self):
        return GarfResponseMessage(to=self.to, from_who=self.from_who, 
                                   title=self.title, message=self.message,
                                   image=self.image, id=self.key.id(), date=self.date)
        
    def to_response_message_by_projection(self, select_projection):
        result = GarfResponseMessage()
        for prop_name in select_projection:
            result.__setattr__(prop_name, getattr(self, prop_name))
        return result