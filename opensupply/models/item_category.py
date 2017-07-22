

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

from datetime import datetime
from .meta import Base
from .meta import DBSession

class ItemCategory(Base):
    
    __tablename__ = "item_categories"

    id = Column("id", Integer, Sequence("supplier_id_seq"), primary_key = True)
    name = Column("name", String)
    notes = Column("notes", String(200), nullable = True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable = True)
    created_on = Column(DateTime, default = datetime.now())
    modified_by = Column(Integer, ForeignKey("users.id"), nullable = True)
    modified_on = Column(DateTime, default = datetime.now(), onupdate = datetime.now())

    branches = relationship("ItemCategoryBranch")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<ItemCategory: %d, %s>" % (self.id, self.name)

    __table_args__ = (UniqueConstraint("name"),)

    @property
    def to_dict(self):
        return {
            "id":          self.id,
            "name":        self.name,
            "notes":       self.notes
            #"created_by":  self.created_by,
            #"created_on":  dump_datetime(self.created_on),
            #"created_on":  datetime(self.created_on),
            #"modified_by": self.modified_by,
            #"modified_on": datetime(self.modified_on),
        }

    def next(self):
        return DBSession.query(ItemCategory).filter(ItemCategory.id > self.id).\
          order_by(ItemCategory.id).first()


    def previous(self):
        return DBSession.query(ItemCategory).filter(ItemCategory.id < self.id).\
          order_by(desc(ItemCategory.id)).first()

