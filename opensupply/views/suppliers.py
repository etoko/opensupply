
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
    print(request)


def _create(self):
    """
    Create new supplier
    """
    pass

def _update(self):
    """
    Update a new supplier
    """
    pass

@view_config(route_name="supplier_save", renderer="string")
def supplier_save(request):
    """
    Called after user clicks save button
    """
    _update if supplier_id == -1 else _create


def supplier_delete(request):
    """
    Called to invoke a delete operation
    """
    pass
