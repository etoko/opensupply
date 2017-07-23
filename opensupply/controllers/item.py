#!/usr/bin/env python
__author__ = "Emmanuel Toko <http://emmanueltoko.blogspot.com><github.com/etoko>"
#date 2017-07-23

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
from opensupply.models import DBSession, Base, Item

class ItemController(ApiController):
    item_id_key = item_name_key = user_controller = None

    def __init__(self):
        item_id_key = "item_id"
        item_name_key = "item_name"
        user_controller = UserController()

    def _to_json(self, item):
        j_item = {
            "id": item.id,
            "name": item.name,
            "notes": item.notes
        }
         
        return json.dumps(j_item, sort_keys=True, indent=4)

    def _validate(j_item):
        """
        Check the validity of a Item instance returning true 
        if valid, otherwise false. Throws a KeyError
        """
        item_id = None
        item_name = None
        
        try:
            item_id = j_item[item_id_key]
        except KeyError:
            raise KeyError("item Id not submitted")
        try:
            item_name = j_item[item_name_key]
        except KeyError:
            raise KeyError("No item name entered")
    
        return True if item_name and item_id else False
    
    def save(self, j_item):
        """
        Place a Item in the Session.
        Its state will be persisted to the database on the next flush operation.
        """
        #if not _validate(j_item):
        #    raise ValueError("Invalid item")
    
        item_id = j_item["id"]
        name = j_item['name']
        username = None #j_item["item_username"]
        user = None #user_controller.get(username = username)[0]
        notes = j_item["notes"]

  
        def _create():
            with transaction.manager:
                item = Item(name)
                item.notes = notes
                item.created_by = user
                item.modified_by = user
                j_item = DBSession.add(item)
                j_item = self.get(LAST=True)
                return j_item
                #region_invalidate(_all, "hour")
      
        def _update():
            with transaction.manager:
                item = DBSession.query(Item).get(item_id)
                if item is None:
                    _create()
                
                item.name = name
                item.notes = notes
                item.modified_by = user #user.id
                item = DBSession.merge(item)
                #region_invalidate(_add)
                return self._to_json(item)

        try:
            item_id = int(item_id)
        except ValueError as verror: 
            #user is creating new Item before clicking n"New" button
            item_id = 0
          
        if (item_id == -1) or (item_id == 0):
            try:
                return _create()
            except IntegrityError as ierror: #Duplicate value
                raise RuntimeError("Duplicate value") from ierror
                #TODO More duplicate value handling capability
        else:
            return _update()
 
        j_item = self._to_json(item)

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
            internal method to navigate to the first item
            """
            item = DBSession.query(Item).order_by(Item.id).first()
            
            return self._to_json(item)


        def _last():
            """
            Navigate to last item
            """ 
            item = DBSession.query(Item).\
                order_by(desc(Item.id)).first()
            return self._to_json(item)
        
        def _all():
            items = DBSession.query(Item).all()

            return items
        

        if args:
            s_id = args[0]
            try:
                s_id = int(s_id)
                item = DBSession.query(Item).get(s_id);
                
               # return self._to_json(item)
                return item
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

    
    @cache_region("hour", "items")
    def _all(self):
        """
        Return all items
        """
        users = DBSession.query(Item).order_by(Item.id). \
                options(joinedload("branches")).all() or None
        return users
    
    def delete(self, item):
        """
        Mark a Item as deleted.
        The database delete operation occurs upon flush().
        """
        item = DBSession.query(Item).get(item.id)
        #next_item = item.next()
        if not item: 
            raise ValueError("Did not find Item")

        #if _validate(item):
        with transaction.manager:
            DBSession.delete(item)
            return True
        
        return False #delete operation failed
        

