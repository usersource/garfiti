'''
Created on 30.10.2013
@author: Sergey Gadzhilov
'''

from protorpc import messages, message_types

class InsertRequestMessage(messages.Message):
    to = messages.StringField(1, required=True)
    from_who = messages.StringField(2, required=True)
    title = messages.StringField(3, required=True)
    message = messages.StringField(4, required=True)
    image = messages.StringField(5, required=True)
    
class InsertResponseMessage(messages.Message):
    id = messages.IntegerField(1)

class GarfResponseMessage(messages.Message):
    to = messages.StringField(1)
    from_who = messages.StringField(2)
    title = messages.StringField(3)
    message = messages.StringField(4)
    image = messages.StringField(5)
    id = messages.IntegerField(6)
    date = message_types.DateTimeField(7)
    
class GarfListResponseMessage(messages.Message):
    garf_list = messages.MessageField(GarfResponseMessage, 1, repeated=True)
    cursor = messages.StringField(2)
    has_more = messages.BooleanField(3)

        