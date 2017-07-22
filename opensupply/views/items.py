
import json
from datetime import datetime
import transaction

from pyramid.httpexceptions import (
                                   exception_response,
                                   HTTPFound,
                                   HTTPNotFound,
                                   HTTPForbidden,
                                   )
from pyramid.renderers import render_to_response
from pyramid.response import Response
from pyramid.static import static_view
from pyramid.security import authenticated_userid, forget, remember
from pyramid.view import view_config

from sqlalchemy.exc import IntegrityError

from opensupply.controllers import (
                            SupplierController, 
                            DepartmentController,
                            UserController, 
                            PermissionController,
                            )
from opensupply.security import USERS
from opensupply.models import User
from opensupply.util import operations
from opensupply.models import DBSession

item_controller = SupplierController()
user_controller = UserController()
permission_controller = PermissionController()
department_controller = DepartmentController()

@view_config(route_name="items_page", renderer="items.mako")
def items_page(request):
    return {"items": "Items"} 

@view_config(route_name = "items_first", renderer="json")
def item_first(request):
    """
    View to navigate to the first item
    """
    item = item_controller.get(FIRST=True)
    print(item)

    return item

@view_config(route_name="items_previous", renderer="json")
def item_previous(request):
    """
    Navigate to previous item
    """
#    item_id = request.params["item_id"]
#    item_id = int(item_id)
#    item_id = item_id - 1
#    item = item_controller.get(item_id)

    item_id = request.params["item_id"]
    item_id = int(item_id)
    item = item_controller.get(item_id)
    item = item.previous()
    j_item = json.dumps(item.to_dict)

    return j_item


@view_config(route_name="items_next", renderer="json")
def item_next(request):
    """
    Navigate to previous item
    """
    item_id = request.params["item_id"]
    item_id = int(item_id)
    #item_id = item_id + 1
    item = item_controller.get(item_id)
    item = item.next()
    j_item = json.dumps(item.to_dict)

    return j_item


@view_config(route_name="items_last", renderer="json")
def item_last(request):
    """
    View to navigate to the last item
    """
    item = item_controller.get(LAST=True)
    
    return item


@view_config(route_name="items_save", renderer="json")
def item_save(request):
    """
    Called after user clicks save button
    """
    j_item = None
    item_id  = request.params['item_id']  
    name  = request.params['item_name']
    tel_1 = request.params['item_tel_1']
    tel_2 = request.params['item_tel_2']
    email = request.params['item_email']
    website = request.params["item_website"]
    fax   = request.params['item_fax']
    address = request.params['item_address']
    notes   = request.params['item_notes']
    
    j_item = {
        'id'  : item_id,
        'name':  name,
        'tel_1': tel_1,
        'tel_2': tel_2,
        'email': email,
        "website": website,
        'fax': fax,
        'address': address,
        'notes': notes 
    }

    item = item_controller.save(j_item)
    
    return item

@view_config(route_name="items_delete", renderer="json")
def item_delete(request):
    """
    Called to invoke a delete operation
    """
    item_id = request.params["item_id"]
    item = item_controller.get(item_id)
    next_item = item.next()
    print(next_item)
 
    if item_controller.delete(item):
        return json.dumps(next_item.to_dict)
    
    
