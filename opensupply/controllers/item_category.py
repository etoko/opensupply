
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
from opensupply.models import DBSession, Base, ItemCategory

class ItemCategoryController(ApiController):
    item_category_id_key = item_category_name_key = user_controller = None

    def __init__(self):
        item_category_id_key = "item_category_id"
        item_category_name_key = "item_category_name"
        user_controller = UserController()

    def _to_json(self, item_category):
        j_item_category = {
            "id": item_category.id,
            "name": item_category.name,
            "notes": item_category.notes
        }
         
        return json.dumps(j_item_category, sort_keys=True, indent=4)

    def _validate(j_item_category):
        """
        Check the validity of a ItemCategory instance returning true 
        if valid, otherwise false. Throws a KeyError
        """
        item_category_id = None
        item_category_name = None
        
        try:
            item_category_id = j_item_category[item_category_id_key]
        except KeyError:
            raise KeyError("item_category Id not submitted")
        try:
            item_category_name = j_item_category[item_category_name_key]
        except KeyError:
            raise KeyError("No item_category name entered")
    
        return True if item_category_name and item_category_id else False
    
    def save(self, j_item_category):
        """
        Place a ItemCategory in the Session.
        Its state will be persisted to the database on the next flush operation.
        """
        #if not _validate(j_item_category):
        #    raise ValueError("Invalid item_category")
    
        item_category_id = j_item_category["id"]
        name = j_item_category['name']
        username = None #j_item_category["item_category_username"]
        user = None #user_controller.get(username = username)[0]
        notes = j_item_category["notes"]

  
        def _create():
            with transaction.manager:
                item_category = ItemCategory(name)
                item_category.notes = notes
                item_category.created_by = user
                item_category.modified_by = user
                j_item_category = DBSession.add(item_category)
                j_item_category = self.get(LAST=True)
                return j_item_category
                #region_invalidate(_all, "hour")
      
        def _update():
            with transaction.manager:
                item_category = DBSession.query(ItemCategory).get(item_category_id)
                if item_category is None:
                    _create()
                
                item_category.name = name
                item_category.notes = notes
                item_category.modified_by = user #user.id
                item_category = DBSession.merge(item_category)
                #region_invalidate(_add)
                return self._to_json(item_category)

        print("CATEGORY ID: " + item_category_id)
        try:
            item_category_id = int(item_category_id)
        except ValueError as verror: 
            #user is creating new ItemCategory before clicking n"New" button
            item_category_id = 0
          
        if (item_category_id == -1) or (item_category_id == 0):
            try:
                return _create()
            except IntegrityError as ierror: #Duplicate value
                raise RuntimeError("Duplicate value") from ierror
                #TODO More duplicate value handling capability
        else:
            return _update()
 
        j_item_category = self._to_json(item_category)

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
            internal method to navigate to the first item_category
            """
            item_category = DBSession.query(ItemCategory).order_by(ItemCategory.id).first()
            
            return self._to_json(item_category)


        def _last():
            """
            Navigate to last item_category
            """ 
            item_category = DBSession.query(ItemCategory).\
                order_by(desc(ItemCategory.id)).first()
            return self._to_json(item_category)
        
        def _all():
            item_categories = DBSession.query(ItemCategory).all()

            return item_categories
        

        if args:
            s_id = args[0]
            try:
                s_id = int(s_id)
                item_category = DBSession.query(ItemCategory).get(s_id);
                
               # return self._to_json(item_category)
                return item_category
            except TypeError as err:
                print(err)
        elif kwargs: 

            if "FIRST" in kwargs:
                return _first()
            elif "LAST" in kwargs:
                return _last()
        else:
            return _all()
        
        return None

    
    @cache_region("hour", "item_categories")
    def _all(self):
        """
        Return all item_categories
        """
        users = DBSession.query(ItemCategory).order_by(ItemCategory.id). \
                options(joinedload("branches")).all() or None
        return users
    
    def delete(self, item_category):
        """
        Mark a ItemCategory as deleted.
        The database delete operation occurs upon flush().
        """
        item_category = DBSession.query(ItemCategory).get(item_category.id)
        #next_item_category = item_category.next()
        if not item_category: 
            raise ValueError("Did not find ItemCategory")

        #if _validate(item_category):
        with transaction.manager:
            DBSession.delete(item_category)
            return True
        
        return False #delete operation failed
        

