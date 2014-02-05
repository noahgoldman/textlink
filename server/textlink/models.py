from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, UniqueConstraint, ForeignKeyConstraint, Index
from sqlalchemy.orm import relationship, backref

from textlink import Base

class Entry(Base):
    __tablename__ = 'entries'
    __table_args__ =  (
            UniqueConstraint('list_id','phone_id'),
            Index('entry_id','list_id','phone_id')
            )
    
    entry_id = Column(Integer, primary_key=True)  
    list_id = Column(Integer, ForeignKey('lists.list_id'))
    phone_id = Column(Integer, ForeignKey('phones.phone_id'))

    
    fields = ['entry_id', 'list_id','phone_id']
    def __init__(self, lid, pid):
        self.list_id = lid
        self.phone_id = pid
    

class Phone(Base):
    __tablename__ = 'phones'

    phone_id = Column(Integer, primary_key=True)
    number = Column(String, unique=True)
    name = Column(String)
    textemail = Column(String)
    entries = relationship("Entry", backref="phone")
    
    fields = ['phone_id', 'number', 'name', 'textemail']

    def __init__(self, name, number):
        self.name = name
        self.number = number

class List(Base):
    __tablename__ = 'lists'

    list_id = Column(Integer, primary_key=True)
    name = Column(String)
    entries = relationship("Entry", backref="list")

    fields = ['list_id', 'name']

    def __init__(self, name):
        self.name = name
