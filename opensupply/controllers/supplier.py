#!/usr/bin/env python
__author__ = "Emmanuel Toko <http://emmanueltoko.blogspot.com><github.com/etoko>"
#date 2012-03-02

import os
import sys
import transaction
import json

from beaker.cache import cache_region, region_invalidate

from sqlalchemy import desc
from sqlalchemy import engine_from_config
from sqlalchemy.orm import joinedload
from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )
from sqlalchemy.exc import IntegrityError

from opensupply.controllers import ApiController
from opensupply.controllers import UserController
from opensupply.models import DBSession, Base, Supplier, SupplierBranch

class SupplierController(ApiController):
    supplier_id_key = supplier_name_key = user_controller = None

    def __init__(self):
        supplier_id_key = "supplier_id"
        supplier_name_key = "supplier_name"
        user_controller = UserController()

    def _to_json(self, supplier):
        j_supplier = {
            "id": supplier.id,
            "name": supplier.name,
            "tel_1": supplier.tel_1,
            "tel_2": supplier.tel_2,
            "email": supplier.email,
             "website": supplier.website,
            "fax": supplier.fax,
            "address": supplier.address,
            "notes": supplier.notes
        }
         
        return json.dumps(j_supplier, sort_keys=True, indent=4)

    def _validate(j_supplier):
        """
        Check the validity of a Supplier instance returning true 
        if valid, otherwise false. Throws a KeyError
        """
        supplier_id = None
        supplier_name = None
        
        try:
            supplier_id = j_supplier[supplier_id_key]
        except KeyError:
            raise KeyError("supplier Id not submitted")
        try:
            supplier_name = j_supplier[supplier_name_key]
        except KeyError:
            raise KeyError("No supplier name entered")
    
        return True if supplier_name and supplier_id else False
    
    def save(self, j_supplier):
        """
        Place a Supplier in the Session.
        Its state will be persisted to the database on the next flush operation.
        """
        #if not _validate(j_supplier):
        #    raise ValueError("Invalid supplier")
    
        supplier_id = j_supplier["id"]
        name = j_supplier['name']
        username = None #j_supplier["supplier_username"]
        user = None #user_controller.get(username = username)[0]
        tel_1 = j_supplier["tel_1"]
        tel_2 = j_supplier["tel_2"]
        fax = j_supplier["fax"]
        email = j_supplier["email"]
        website = j_supplier["website"]
        address = j_supplier["address"]
        notes = j_supplier["notes"]

  
        def _create():
            with transaction.manager:
                supplier = Supplier(name)
                supplier.tel_1 = tel_1
                supplier.tel_2 = tel_2
                supplier.fax = notes
                supplier.email = email
                supplier.address = address
                supplier.notes = notes
                supplier.website = website
                supplier.created_by = user
                supplier.modified_by = user
                j_supplier = DBSession.add(supplier)
                j_supplier = self.get(LAST=True)
                return j_supplier
                #region_invalidate(_all, "hour")
      
        def _update():
            with transaction.manager:
                supplier = DBSession.query(Supplier).get(supplier_id)
                if supplier is None:
                    _create()
                
                supplier.name = name
                supplier.tel_1 = tel_1
                supplier.tel_2 = tel_2
                supplier.fax = fax
                supplier.email = email
                supplier.website = website
                supplier.address = address
                supplier.notes = notes
                supplier.modified_by = user #user.id
                supplier = DBSession.merge(supplier)
                #region_invalidate(_add)
                return self._to_json(supplier)


        try:
            supplier_id = int(supplier_id)
        except ValueError as verror:
            supplier_id = 0

        if (supplier_id == -1) or (supplier_id == 0):
            try:
                return _create()
            except IntegrityError as ierror: #Duplicate value
                raise RuntimeError("Duplicate value") from ierror
                #TODO More duplicate value handling capability
        else:
            return _update()
 
        j_supplier = self._to_json(supplier)

        return None

     
    def get(self, *args, **kwargs):
        """
        Copy the state an instance onto the persistent instance with the same 
        identifier.
        If there is no persistent instance currently associated with the 
        session, it will be loaded. Return the persistent instance. If the 
        given instance is unsaved, save a copy of and return it as a newly 
        persistent instance. The given instance does not become associated 
        with the session.
        """

        
        def _first():
            """
            internal method to navigate to the first supplier
            """
            supplier = DBSession.query(Supplier).order_by(Supplier.id).first()
            
            return self._to_json(supplier)


        def _last():
            """
            Navigate to last supplier
            """ 
            supplier = DBSession.query(Supplier).\
                order_by(desc(Supplier.id)).first()
            return self._to_json(supplier)
        
        if args:
            s_id = args[0]
            try:
                s_id = int(s_id)
                supplier = DBSession.query(Supplier).get(s_id);
                
               # return self._to_json(supplier)
                return supplier
            except TypeError as err:
                print(err)
        elif kwargs: 

            if "FIRST" in kwargs:
                return _first()
            elif "LAST" in kwargs:
                return _last()
        
        return None

    
    @cache_region("hour", "suppliers")
    def _all(self):
        """
        Return all suppliers
        """
        users = DBSession.query(Supplier).order_by(Supplier.id). \
                options(joinedload("branches")).all() or None
        return users
    
    def delete(self, supplier):
        """
        Mark a Supplier as deleted.
        The database delete operation occurs upon flush().
        """
        supplier = DBSession.query(Supplier).get(supplier.id)
        #next_supplier = supplier.next()
        if not supplier: 
            raise ValueError("Did not find Supplier")

        #if _validate(supplier):
        with transaction.manager:
            DBSession.delete(supplier)
            return True
        
        return False #delete operation failed
        
    def save_branch(self, j_branch):
        """
        Create/update a supplier branch
        """
        global supplier_id_key 
        supplier_id_key = "supplier_id"
        if not isinstance(j_branch, dict): 
            import json
            j_branch = json.loads(j_branch) 
        branch_id = j_branch.pop("supplier_branch_id", None)
        print(j_branch[supplier_id_key])
        supplier_id = j_branch.pop(supplier_id_key, None)
        if not supplier_id: raise TypeError("No Supplier Set")

        def _setattr(branch):
            branch.id = branch_id
            if branch.id is None: raise TypeError("Branch id not set")
            branch.street_address = \
                       j_branch.pop("supplier_branch_street_address", None)
            branch.tel_1 = j_branch.pop("supplier_branch_tel_1", None)
            branch.tel_2 = j_branch.pop("supplier_branch_tel_2", None)
            branch.email_address = j_branch.pop("supplier_branch_email", None)
            branch.website = j_branch.pop("supplier_branch_website", None)
            return branch
            
        def _create():
            supplier = DBSession.query(Supplier).get(supplier_id)
            print(supplier.to_json)
            if supplier is None:
                raise TypeError(
                       "Could not find supplier with id: %s" % supplier_id)
            branch = SupplierBranch(supplier_id)
            branch =_setattr(branch)
            del branch.id
            with transaction.manager:
                DBSession.add(branch)
     
        def _update():
            branch = DBSession.query(SupplierBranch).get(branch_id)
            branch = _setattr(branch)
            with transaction.manager:
                DBSession.merge(branch)
    
        _create() if branch_id == -1 else _update()
        region_invalidate(self._all, "hour", "suppliers")
    
    def delete_branch(self, j_branch):
        branch_id = j_branch.pop("suppliers_branch_id", None)
        if not branch_id: raise KeyError("Invalid Branch")
        branch = DBSession.query(SupplierBranch).get(branch_id)
        with transaction.manager:
            DBSession.delete(branch)

    def _validate_branch(j_branch):
        if j_branch:
            if j_branch["bank_branch_id"] and \
                    j_branch["bank_branch_"]:
                return True
        return False

    def save_item(self, j_item):
        """
        Persist an item.
        """
        item_id = j_item.pop("s_branch_item_id", None)

        def _setattr(item):
            measurement = j_item.pop("s_branch_item_measurement", None)
            category = j_item.pop("s_branch_item_category", None)
            supplier = j_item.pop("s_branch", None)
            vat_inclusive = j_item.pop("s_branch_vat", None)
            created_by = j_item.pop("s_branch_created_by", None)
            created_on = j_item.pop("s_branch_created_on", None)
            modfied_by = j_item.pop("s_branch_modified_by", None)

        def _create():
            _setattr(item)
        
        def _update():
            item = DBSession.query(Item).get(item_id)
            _setattr(item)
            with transaction.manager:
                DBSession.merge(item)
                return True

        _create() if item_id is not None and item_id > 0 else _update
        return False
