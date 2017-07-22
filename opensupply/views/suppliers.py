
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

supplier_controller = SupplierController()
user_controller = UserController()
permission_controller = PermissionController()
department_controller = DepartmentController()


@view_config(route_name = "suppliers_first", renderer="json")
def supplier_first(request):
    """
    View to navigate to the first supplier
    """
    supplier = supplier_controller.get(FIRST=True)
    print(supplier)

    return supplier

@view_config(route_name="suppliers_previous", renderer="json")
def supplier_previous(request):
    """
    Navigate to previous supplier
    """
#    supplier_id = request.params["supplier_id"]
#    supplier_id = int(supplier_id)
#    supplier_id = supplier_id - 1
#    supplier = supplier_controller.get(supplier_id)

    supplier_id = request.params["supplier_id"]
    supplier_id = int(supplier_id)
    supplier = supplier_controller.get(supplier_id)
    supplier = supplier.previous()
    j_supplier = json.dumps(supplier.to_dict)

    return j_supplier


@view_config(route_name="suppliers_next", renderer="json")
def supplier_next(request):
    """
    Navigate to previous supplier
    """
    supplier_id = request.params["supplier_id"]
    supplier_id = int(supplier_id)
    #supplier_id = supplier_id + 1
    supplier = supplier_controller.get(supplier_id)
    supplier = supplier.next()
    j_supplier = json.dumps(supplier.to_dict)

    return j_supplier


@view_config(route_name="suppliers_last", renderer="json")
def supplier_last(request):
    """
    View to navigate to the last supplier
    """
    supplier = supplier_controller.get(LAST=True)
    
    return supplier


@view_config(route_name="suppliers_save", renderer="json")
def supplier_save(request):
    """
    Called after user clicks save button
    """
    j_supplier = None
    supplier_id  = request.params['supplier_id']  
    name  = request.params['supplier_name']
    tel_1 = request.params['supplier_tel_1']
    tel_2 = request.params['supplier_tel_2']
    email = request.params['supplier_email']
    website = request.params["supplier_website"]
    fax   = request.params['supplier_fax']
    address = request.params['supplier_address']
    notes   = request.params['supplier_notes']
    
    j_supplier = {
        'id'  : supplier_id,
        'name':  name,
        'tel_1': tel_1,
        'tel_2': tel_2,
        'email': email,
        "website": website,
        'fax': fax,
        'address': address,
        'notes': notes 
    }

    supplier = supplier_controller.save(j_supplier)
    
    return supplier

@view_config(route_name="suppliers_delete", renderer="json")
def supplier_delete(request):
    """
    Called to invoke a delete operation
    """
    supplier_id = request.params["supplier_id"]
    supplier = supplier_controller.get(supplier_id)
    next_supplier = supplier.next()
    print(next_supplier)
 
    if supplier_controller.delete(supplier):
        return json.dumps(next_supplier.to_dict)
    
    
