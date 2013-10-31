'''
Created on 30.10.2013
@author: Sergey Gadzhilov
'''

import endpoints
from protorpc import remote, message_types, messages
from garfiti_api_messages import InsertRequestMessage
from garfiti_api_messages import InsertResponseMessage
from garfiti_api_messages import GarfResponseMessage
from garfiti_api_messages import GarfListResponseMessage
from model.GarfModel import GarfModel

from google.appengine.datastore.datastore_query import Cursor
from google.appengine.ext.db import BadValueError


@endpoints.api(name="garfiti", 
               version="v1", 
               description="Garfiti api", 
               allowed_client_ids=[endpoints.API_EXPLORER_CLIENT_ID])
class GarfitiApi(remote.Service):
    
    @endpoints.method(InsertRequestMessage, 
                      InsertResponseMessage,
                      path="garf",
                      http_method="POST",
                      name="garf.insert")
    def AddGarfiti(self, request):
        
        garfiti = GarfModel(to=request.to,
                            from_who=request.from_who,
                            title=request.title,
                            message=request.message,
                            image = request.image)
        garfiti.put()
        return InsertResponseMessage(id=garfiti.key.id())
    
    GetGarfRequest = endpoints.ResourceContainer(
        message_types.VoidMessage,
        id=messages.IntegerField(2, required=True),
        include_props=messages.StringField(3)
    ) 
    
    @endpoints.method(GetGarfRequest, 
                      GarfResponseMessage,
                      path="garf/{id}",
                      http_method="GET",
                      name="garf.get")
    def GetGarfiti(self, request):
        
        if request.id is None:
            raise endpoints.BadRequestException('id field is required.')
        garfiti = GarfModel.get_by_id(request.id)
        
        if garfiti is None:
            raise endpoints.NotFoundException('No anno entity with the id "%s" exists.' % request.id)
        
        select_projection = None
        if request.include_props is not None:
            select_projection = request.include_props.split(',')
            
        if select_projection is not None:
            result = garfiti.to_response_message_by_projection(select_projection)
        else:
            result = garfiti.to_response_message()
        return result
    
    
    GarfListRequest = endpoints.ResourceContainer(
        message_types.VoidMessage,
        feq_to=messages.StringField(2),
        cursor=messages.StringField(3),
        limit=messages.IntegerField(4),
        include_props=messages.StringField(5)
        
    )
    @endpoints.method(GarfListRequest, 
                      GarfListResponseMessage,
                      path="garfs",
                      http_method="GET",
                      name="garf.list")
    def GetGarfitiList(self, request):
        
        limit = 10
        
        if request.limit is not None:
            limit = request.limit

        curs = None
        if request.cursor is not None:
            try:
                curs = Cursor(urlsafe=request.cursor)
            except BadValueError:
                raise endpoints.BadRequestException('Invalid cursor %s.' % request.cursor)

        select_projection = None
        if request.include_props is not None:
            select_projection = request.include_props.split(',')
        
        hQuery = None
        if request.feq_to is not None:
            hQuery = GarfModel.query(GarfModel.to == request.feq_to)
        else:
            hQuery = GarfModel.query()
                
        if (curs is not None):
            garfs, next_curs, more = hQuery.fetch_page(limit, start_cursor=curs)
        else:
            garfs, next_curs, more = hQuery.fetch_page(limit)            
        
        items = None
        if select_projection is not None:
            items = [entity.to_response_message_by_projection(select_projection) for entity in garfs]
        else:
            items = [entity.to_response_message() for entity in garfs]

        if more:
            return GarfListResponseMessage(garf_list=items, cursor=next_curs.urlsafe(), has_more=more)
        else:
            return GarfListResponseMessage(garf_list=items, has_more=more)
        

application = endpoints.api_server([GarfitiApi], restricted=False)
            