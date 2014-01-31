from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref

from textlink import Base

class Entry(Base):
    __tablename__ = 'entries'

    entry_id = Column(Integer, primary_key=True)  
    mlist = Column(Integer, ForeignKey('lists.list_id'), primary_key=True)
    mphone = Column(Integer, ForeignKey('phones.phone_id'), primary_key=True)

    fields = ['entry_id', 'mlist','mphone']
    
    def __init__(self, list_, phone):
        self.mlist = list_
        self.mphone = phone      

class Phone(Base):
    __tablename__ = 'phones'

    phone_id = Column(Integer, primary_key=True)
    number = Column(Integer, unique=True)
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
