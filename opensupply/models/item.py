#!/usr/bin/env python

from datetime import datetime

from sqlalchemy import (
    Column,
    Boolean,
    Integer,
    Text,
    Sequence,
    DateTime,
    String,
    ForeignKey,
    Table,
    UniqueConstraint,
    )

from sqlalchemy import desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, column_property

from zope.sqlalchemy import ZopeTransactionExtension
from pyramid.security import (
  Allow,
  Everyone,
  )

from .meta import Base, DBSession


class Item(Base):

    __tablename__ = "items"

    id = Column(Integer, Sequence("item_id_seq"), primary_key = True)
    name = Column(String(50))
    unit_of_measurement = Column(String(50))
    category = Column(ForeignKey("item_categories.id"))
    vat_inclusive = Column(Boolean)
    notes = Column(Text)
    created_by = Column(ForeignKey("users.id"))
    created_on = Column(DateTime, default = datetime.now())
    modified_by = Column(ForeignKey("users.id"))
    modified_on = Column(DateTime, default = datetime.now(), 
      onupdate = datetime.now())

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Item: %d, %s, %d>" % (self.id, self.name, self.category)

    def next(self):
        return DBSession.query(Item).filter(Item.id > self.id).\
            order_by(Item.id).first()

    def previous(self):
        return DBSession.query(Item).filter(Item.id < self.id).\
            order_by(desc(Item.id)).first()

    @property
    def to_dict(self):
        return {
            "id":                  self.id,
            "name":                self.name,
            "unit_of_measurement": self.unit_of_measurement,
            "category":            self.category,
            "vat_inclusive":       self.vat_inclusive,
            "created_by":          self.created_by,
           # "created_on":          self.created_on,
            "modified_by":         self.modified_by,
           # "modified_date":       self.modified_on
        }


