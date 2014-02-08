from flask import request
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError, IntegrityError
from textlink import app, Session
from textlink.models import Entry, Phone, List, PhoneCarrier
from textlink.Obj2JSON import jsonobj
from textlink.helpers import API
from textlink.sources.sendByTwilio import sendSMS
from textlink.sources.emailgateway import *

@app.route('/')
def index():
    return "Hello World!"

@app.route('/lists/add', methods=['POST'])
@API
def create_list():
    name = request.form.get('name')
    lst = List(name)
    
    session = Session()
    session.add(lst)
    session.commit()

    return jsonobj(lst)

#Gets all Phones
@app.route('/entries/getAll', methods=['GET']) #for Testing:
def getAllEntries():
    session = Session()
    es = session.query(Entry).all()
    es = jsonobj(es)
    return es

#Gets all Phones
@app.route('/phones/getAll', methods=['GET']) #for Testing:
def getAllPhones():
    session = Session()
    es = session.query(Phone).all()
    es = jsonobj(es)
    return es

#Takes a phone ID and tells you all the entries it is in
#I think this will be useful because you can find out what lists a specific phone is in
@app.route('/phones/<phone_id>/allEntries', methods=['GET']) #for Testing:
def getPhoneEntries(phone_id):
    session = Session()
    es = session.query(Entry).filter_by(phone_id=phone_id).all()
    es = jsonobj(es)
    return es

#Gets name and number based on phone_id
@app.route('/phones/<phone_id>', methods=['GET']) #for Testing:
def getPhoneInfo(phone_id):
    session = Session()
    es = session.query(Phone).filter_by(phone_id=phone_id).all()
    es = jsonobj(es)
    return es

#Returns a list of all the Lists in the db
@app.route('/lists/getAll', methods=['GET']) #for Testing:
def getLists():
    session = Session()
    es = session.query(List).all()
    es = jsonobj(es)
    return es
    
#Gets all entries in a list
@app.route('/lists/<list_id>', methods=['GET']) #for Testing:
def list_list(list_id):
    session = Session()
    try:
        es = session.query(Entry).filter_by(list_id=list_id).all()
    except NoresultFound:
        return None
    else: 
        es = jsonobj(es)
        return es

@app.route('/phones/', methods=['GET']) #for Testing:
def get_phones():
    session = Session()
    try:
        es = session.query(Phone).all()
    except NoresultFound:
        return None
    else: 
        es = jsonobj(es)
        return es
    
@app.route('/phones/<phone_id>/carriers', methods=['GET']) #for Testing:
def get_carriers(phone_id):
    session = Session()
    try:
        es = session.query(Phone).filter_by(phone_id=phone_id).one()
    except NoresultFound:
        return None
    else: 
        carriers = session.query(PhoneCarrier).filter_by(phone_id=phone_id).all()
        return jsonobj(carriers)

    
#Adds an entry to a list
@app.route('/lists/<list_id>/add', methods=['POST']) #for Testing:
def add_user(list_id):
    
    num = request.form.get('number')
    name = request.form.get('name')
    session = Session()
    email = ""
    try:
        phone = session.query(Phone).filter_by(number=num).one()
    except NoResultFound:
        phone = Phone(name,int(num))
        session.add(phone)
        session.commit()
        init_possible_carriers(num)
    
    entry = Entry(list_id, phone.phone_id)
    
    try:
        session.add(entry)
        session.commit()
    except (IntegrityError,InvalidRequestError):
        Session.rollback()
        return "Phone already exists for this list"
    else: 
        return jsonobj(entry)

@app.route('/lists/<list_id>/send_email',methods=['POST'])
def send_text(list_id):
    sender = request.form.get('sender')
    print sender
    message = request.form.get('message')
    session = Session()
    lst = session.query(List).get(list_id)
    #attachments = request.form.get('attachments')
    print message
    for phone in lst.entries:
        
        #text_by_email(phone.number, sender, message, phone.textemail)

@app.route('/lists/<list_id>/send_twilio',methods=['POST'])
def send_text_Twilio(list_id):
    sender = request.form.get('sender')
    print sender
    message = request.form.get('message')

    session = Session()
    lst = session.query(List).get(list_id)
    assert lst
    #attachments = request.form.get('attachments')
    print message
    for entry in lst.entries:
        print "sent message"
        sendSMS("AC0955b5ae6e4e14861d9e1f61e7d0680f","2dc773f8f669503c2dd6021d8b7bf5b7", sender, entry.phone.number, message)
    return "hello"
