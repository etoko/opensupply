

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
                            RequisitionController, 
                            DepartmentController,
                            UserController, 
                            PermissionController,
                            )
from opensupply.security import USERS
from opensupply.models import User
from opensupply.util import operations
from opensupply.models import DBSession

requisition_controller = RequisitionController()
user_controller = UserController()
permission_controller = PermissionController()
department_controller = DepartmentController()


@view_config(route_name = "requisitions_first", renderer="json")
def requisition_first(request):
    """
    View to navigate to the first requisition
    """
    requisition = requisition_controller.get(FIRST=True)
    print(requisition)

    return requisition

@view_config(route_name="requisitions_previous", renderer="json")
def requisition_previous(request):
    """
    Navigate to previous requisition
    """
#    requisition_id = request.params["requisition_id"]
#    requisition_id = int(requisition_id)
#    requisition_id = requisition_id - 1
#    requisition = requisition_controller.get(requisition_id)

    requisition_id = request.params["requisition_id"]
    requisition_id = int(requisition_id)
    requisition = requisition_controller.get(requisition_id)
    requisition = requisition.previous()
    j_requisition = json.dumps(requisition.to_dict)

    return j_requisition


@view_config(route_name="requisitions_next", renderer="json")
def requisition_next(request):
    """
    Navigate to previous requisition
    """
    requisition_id = request.params["requisition_id"]
    requisition_id = int(requisition_id)
    #requisition_id = requisition_id + 1
    requisition = requisition_controller.get(requisition_id)
    requisition = requisition.next()
    j_requisition = json.dumps(requisition.to_dict)

    return j_requisition


@view_config(route_name="requisitions_last", renderer="json")
def requisition_last(request):
    """
    View to navigate to the last requisition
    """
    requisition = requisition_controller.get(LAST=True)
    
    return requisition


@view_config(route_name="requisitions_save", renderer="json")
def requisition_save(request):
    """
    Called after user clicks save button
    """
    j_requisition = None
    requisition_id  = request.params['requisition_id']  
    name  = request.params['requisition_name']
    tel_1 = request.params['requisition_tel_1']
    tel_2 = request.params['requisition_tel_2']
    email = request.params['requisition_email']
    website = request.params["requisition_website"]
    fax   = request.params['requisition_fax']
    address = request.params['requisition_address']
    notes   = request.params['requisition_notes']
    
    j_requisition = {
        'id'  : requisition_id,
        'name':  name,
        'tel_1': tel_1,
        'tel_2': tel_2,
        'email': email,
        "website": website,
        'fax': fax,
        'address': address,
        'notes': notes 
    }

    requisition = requisition_controller.save(j_requisition)
    
    return requisition

@view_config(route_name="requisitions_delete", renderer="json")
def requisition_delete(request):
    """
    Called to invoke a delete operation
    """
    requisition_id = request.params["requisition_id"]
    requisition = requisition_controller.get(requisition_id)
    next_requisition = requisition.next()
    print(next_requisition)
 
    if requisition_controller.delete(requisition):
        return json.dumps(next_requisition.to_dict)
    
    
