
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


@view_config(route_name = "supplier_first", renderer="string")
def supplier_first(request):
    """
    View to navigate to the first supplier
    """
    supplier = supplier_controller.get(FIRST=True)
    print(supplier)

    return supplier


def supplier_last(request):
    """
    View to navigate to the last supplier
    """
    pass #TODO implementation of navigation to last supplier



@view_config(route_name="supplier_save", renderer="string")
def supplier_save(request):
    """
    Called after user clicks save button
    """
    print(request.params)
    j_supplier = None
    s_id  = request.params['supplier_id']  
    name  = request.params['supplier_name']
    tel_1 = request.params['supplier_tel_1']
    tel_2 = request.params['supplier_tel_2']
    email = request.params['supplier_email']
    fax   = request.params['supplier_fax']
    address = request.params['supplier_address']
    notes   = request.params['supplier_notes']
    
    j_supplier = {
        'supplier_id'  : s_id,
        'supplier_name':  name,
        'supplier_tel_1': tel_1,
        'supplier_tel_2': tel_2,
        'supplier_email': email,
        'supplier_fax': fax,
        'supplier_address': address,
        'supplier_notes': notes 
    }

    supplier_controller.save(j_supplier)

def supplier_delete(request):
    """
    Called to invoke a delete operation
    """
    pass
