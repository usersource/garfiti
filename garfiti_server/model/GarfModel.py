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
    message_text = ndb.StringProperty()
    image = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
           
    @classmethod
    def put_from_message(cls, message):
        entity = cls(to=message.to,
                     from_who=message.from_who,
                     title=message.title,
                     message_text=message.message_text,
                     image = message.image)
        entity.put()
        return entity.key.id()
    
    
    def to_response_message(self):
        return GarfResponseMessage(to=self.to, from_who=self.from_who, 
                                   title=self.title, message_text=self.message_text,
                                   image=self.image)
        
    def to_response_message_by_projection(self, select_projection):
        result = GarfResponseMessage()
        for prop_name in select_projection:
            result.__setattr__(prop_name, getattr(self, prop_name))
        return result