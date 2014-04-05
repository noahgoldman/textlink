from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, UniqueConstraint, ForeignKeyConstraint, Index, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
import bcrypt
import uuid
import hmac
import hashlib
import base64

Base = declarative_base()

class Entry(Base):
    __tablename__ = 'entries'
    __table_args__ =  (
            UniqueConstraint('list_id','phone_id'),
            Index('entry_id','list_id','phone_id')
            )
    
    entry_id = Column(Integer, primary_key=True)  
    list_id = Column(Integer, ForeignKey('lists.list_id'))
    phone_id = Column(Integer, ForeignKey('phones.phone_id'))

    
    fields = ['entry_id', 'list_id','phone_id', 'phone']

    def __init__(self, lid, pid):
        self.list_id = lid
        self.phone_id = pid
    
class PhoneCarrier(Base):
    __tablename__ = 'carriers'
    __table_args__ =  (
            UniqueConstraint('phone_id','email'),
            Index('phone_carrier_id','phone_id', 'email')
    )
    phone_carrier_id = Column(Integer, primary_key=True)
    phone_id = Column(Integer, ForeignKey('phones.phone_id'))
    email = Column(String) #Possible Email
    possible = Column(Boolean, default=True)
    
    fields = ['phone_carrier_id', 'phone_id', 'email','possible']
    def __init__(self, phone_id, email):
        self.phone_id = phone_id
        self.email = email
    

class Phone(Base):
    __tablename__ = 'phones'

    phone_id = Column(Integer, primary_key=True)
    number = Column(String, unique=True)
    name = Column(String)
    textemail = Column(String)
    entries = relationship("Entry", backref="phone")
    possible_carriers = relationship("PhoneCarrier", backref="phone")
    
    fields = ['phone_id', 'number', 'name', 'textemail', 'possible_carriers', 'entries']

    def __init__(self, name, number):
        self.name = name
        self.number = number

class List(Base):
    __tablename__ = 'lists'

    list_id = Column(Integer, primary_key=True)
    name = Column(String)
    entries = relationship("Entry", backref="list")

    fields = ['list_id', 'name', 'entries']

    def __init__(self, name):
        self.name = name

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    password = Column(String)

    def __init__(self, name, password):
        self.name = name
        self.password = bcrypt.hashpw(password, bcrypt.gensalt(12))

    def check_pass(self, passw):
        return bcrypt.hashpw(passw, self.password) == self.password

class Key(Base):
    __tablename__ = 'keys'

    key_id = Column(Integer, primary_key=True)
    secret = Column(String)
    user_id = Column(Integer, ForeignKey('users.user_id'))

    def __init__(self, user):
        self.user_id = user.user_id
        self.secret = uuid.uuid4().hex

    def check_signature(self, msg, signature):
        hash = hmac.new(bytes(self.secret), bytes(msg), hashlib.sha256).digest()
        encoded = base64.encodestring(hash).strip()
        return signature == encoded
