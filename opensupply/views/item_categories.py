

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
                            ItemCategoryController,
                            )
from opensupply.security import USERS
from opensupply.models import User
from opensupply.util import operations
from opensupply.models import DBSession

item_category_controller = ItemCategoryController()
user_controller = UserController()
permission_controller = PermissionController()
department_controller = DepartmentController()

@view_config(route_name="item_categories_page", renderer="item_categories.mako")
def item_categories_page(request):
    return {"item_categories": "Item Categories"} 

@view_config(route_name = "item_categories_first", renderer="json")
def item_category_first(request):
    """
    View to navigate to the first item_category
    """
    item_category = item_category_controller.get(FIRST=True)

    return item_category

@view_config(route_name="item_categories_previous", renderer="json")
def item_category_previous(request):
    """
    Navigate to previous item_category
    """
#    item_category_id = request.params["item_category_id"]
#    item_category_id = int(item_category_id)
#    item_category_id = item_category_id - 1
#    item_category = item_category_controller.get(item_category_id)

    item_category_id = request.params["item_category_id"]
    item_category_id = int(item_category_id)
    item_category = item_category_controller.get(item_category_id)
    item_category = item_category.previous()
    j_item_category = json.dumps(item_category.to_dict)

    return j_item_category


@view_config(route_name="item_categories_next", renderer="json")
def item_category_next(request):
    """
    Navigate to previous item_category
    """
    item_category_id = request.params["item_category_id"]
    item_category_id = int(item_category_id)
    #item_category_id = item_category_id + 1
    item_category = item_category_controller.get(item_category_id)
    item_category = item_category.next()
    j_item_category = json.dumps(item_category.to_dict)

    return j_item_category


@view_config(route_name="item_categories_last", renderer="json")
def item_category_last(request):
    """
    View to navigate to the last item_category
    """
    item_category = item_category_controller.get(LAST=True)
    
    return item_category


@view_config(route_name="item_categories_save", renderer="json")
def item_category_save(request):
    """
    Called after user clicks save button
    """
    print(request.params)
    j_item_category = None
    item_category_id  = request.params['item_category_id']  
    name  = request.params['item_category_name']
    notes = request.params['item_category_notes']
    
    j_item_category = {
        'id'  : item_category_id,
        'name':  name,
        'notes': notes 
    }

    item_category = item_category_controller.save(j_item_category)
    
    return item_category

@view_config(route_name="item_categories_all", renderer="json")
def item_category_list(request):
    item_categories = item_category_controller.get()
    item_categories_json = []

    for item_category in item_categories:
        item_categories_json.append(
            item_category.to_dict)

    return {"label":"name", "identifier":"id" , "items": item_categories_json	}
    

@view_config(route_name="item_categories_delete", renderer="json")
def item_category_delete(request):
    """
    Called to invoke a delete operation
    """
    item_category_id = request.params["item_category_id"]
    item_category = item_category_controller.get(item_category_id)
    next_item_category = item_category.next()
    print(next_item_category)
 
    if item_category_controller.delete(item_category):
        return json.dumps(next_item_category.to_dict)
    
    
