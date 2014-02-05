from flask import request
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError, IntegrityError
from textlink import app, Session
from textlink.models import Entry, Phone, List
from textlink.Obj2JSON import jsonobj
from textlink.helpers import API
from textlink.sources.sendByTwilio import sendSMS
from textlink.sources.emailgateway import *

@app.route('/')
def index():
    return "Hello World!"

@app.route('/lists', methods=['POST'])
@API
def create_list():
    name = request.form.get('name')
    lst = List(name)
    
    session = Session()
    session.add(lst)
    session.commit()

    return jsonobj(lst)

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
    es = session.query(Entry).filter_by(list_id=list_id).all()
    es = jsonobj(es)
    return es
    
#Adds an entry to a list
@app.route('/lists/<list_id>/add', methods=['POST']) #for Testing:
def add_user(list_id):
    #Need to not allow multiples.
    num = request.form.get('number')
    name = request.form.get('name')
    session = Session()
    email = ""
    try:
        phone = session.query(Phone).filter_by(number=num).one()
    except NoResultFound:
        phone = Phone(name,num)
        phone.textemail = find_email_gateway(phone.number)
        session.add(phone)
        session.commit()
    
    entry = Entry(list_id, phone.phone_id)
    
    try:
        session.add(entry)
        session.commit()
    except (IntegrityError,InvalidRequestError):
        pass
        Session.rollback()
        entry.list_id = -1
        entry.phone_id = -1
        entry.entry_id = -1
        return jsonobj(entry), "Phone already exists for this list"
    else: 
        return jsonobj(entry)

@app.route('/lists/<list_id>/send_email',methods=['POST'])
def send_text(list_id):
    name = request.form.get('name')
    sender = request.form.get('sender')
    print sender
    message = request.form.get('message')
    session = Session()
    lst = session.query(List).get(list_id)
    #attachments = request.form.get('attachments')
    print message
    for phone in lst.phones:
        text_by_email(phone.number, sender, message, phone.textemail)

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
