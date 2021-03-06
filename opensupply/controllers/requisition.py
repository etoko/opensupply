__author__ = "Emmanuel TOKO"

import transaction

from opensupply.models import DBSession, Requisition

from opensupply.controllers import ApiController

from sqlalchemy import desc
from sqlalchemy.types import Boolean

class RequisitionController(ApiController):
    """
    Class manages requistion operations
    """
    id = 0
    requested_date = None
    expected_date = None
    department_id = 0
    requested_by = 0
    requested_date = None
    recommended_by = 0
    recommended_date = None
    approved_by = 0
    approved_date = None
    items = []
    created_by = 0
    created_date = None
    modified_by = 0
    modified_date = None

    def _set_attributes():
        self.id = j_requistion.pop("requisition.id")
        self.request_date = j_requisition.pop("requisition.request_date")
        self.expected_date = j_requisition.pop("requisition.expected_date")
        self.department_id = j_requisition.pop("requisition.department_id")
        self.requested_by = j_requisition.pop("requisition.requested_by")
        self.requested_date = j_requisition.pop("requisition.requested_date")
        self.recommended_by = j_requistion.pop("requistion.recommended_by")
        self.recommended_date = j_requistion.pop("requistion.recommended_date")
        self.approved_by = j_requisition.pop("requisition.approved_by")
        self.approved_date = j_reqisition.pop("requisition.approved_date")
        self.items = j_requisition.pop("requisition.items")
        self.created_by = requisition.pop("requisition.created_by")
        self.created_date = requisition.pop("requisition.created_date")
        self.modified_by = requisition.pop("requisition.modified_by")
        self.modified_date = requisition.pop("requisition.modified_date")

    def _set_requisition(requisition):
        requisition.request_date = self.request_date
        requisition.expected_date = self.expected_date
        requisition.department_id = self.department_id
        requisition.requested_by = self.requested_by
        requisition.requested_date = self.requested_date
        requisition.recommended_by = self.recommended_by
        requisition.recommended_date = self.recommended_date
        requisition.approved_by = self.approved_by
        requisition.approved_date = self.approved_date
        requisition.items = self.items
        requisition.created_by = self.created_by
        requisition.created_date = self.created_date
        requisition.modified_by = self.modified_by
        requisition.modified_date = self.modified_date
        return requisition
        
    def save(self, j_requisition):
        #_set_attributes()
        requisition_id = j_requisition["requisition_id"]
        department_id = j_requisition["department_id"]
        expected_date = j_requisition["expected_date"]
        

        def _create():
            requisition = Requisition()
            #requisition = _set_requisition(requisition)
            requisition.department = department_id
            requisition.expected_date = expected_date

            with transaction.manager:
                DBSession.add(requisition)
                transaction.commit()
 
        def _update():
            with transaction.manager:
                requisition = DBSession.get(requisition.id)
                #requisition = _set_requisition(requisition)
                requisition.department = department_id
                requisition.expected_date = expected_date
                DBSession.merge(requisition)
                transaction.commit()
        

        try:
            requisition_id = int(requisition_id)
            
            if (requisition_id == -1) or (requisition_id == 0):
                _create()
                return self.get(LAST=True)
            else:
                _update()
        except ValueError as v_error:
            #user did not click new button
            _create()


    def get(self, *args, **kwargs):
        """
        Retrieve a specific Requisition model that matches specific criteria 
        i.e. id value submitted a list of requisitions
        """

        def __first():
            requisition = DBSession.query(Requisition).order_by(\
                Requisition.id).first()

            return requisition

        def __last():
            requisition = DBSession.query(Requisition).order_by(\
                desc(Requisition.id)).first()

            return requisition


        if args:
            #if requisition id has been submitted as parameter
            # return Requisition model that matches the id
            try:
                requisition_id = int(args[0])
                requisition = DBSession.query(Requisition).get(requisition_id)

                return requisition
            except ValueError as v_error:
                raise v_error
                #TODO better exception handling

        elif kwargs:
            if "FIRST" in kwargs:
                return __first()
            elif "LAST" in kwargs:
                return __last()
        else: #return all requisitions
            requistions = DBSession.query(Requisition).order_by(\
                Requisition.id).all()
            
            return requisitions

        return None


    def delete(self, requisition_id):
        requisition = get(requisition_id)
        requisition.void = True

        with transaction.manager:
            DBSession.merge(requisition)
            transaction.commit()
