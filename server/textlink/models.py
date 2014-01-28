from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref

from textlink import Base

class Number(Base):
    __tablename__ = 'numbers'

    id = Column(Integer, primary_key=True)
    number = Column(String)

class Phone(Base):
    __tablename__ = 'phones'

    id = Column(Integer, primary_key=True)
    number = Column(Integer, ForeignKey('numbers.id'))
    mlist = Column(Integer, ForeignKey('lists.id'))
    name = Column(String)


class List(Base):
    __tablename__ == 'lists'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    phones = relationship("Phone", backref="list")
