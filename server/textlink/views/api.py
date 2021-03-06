from flask import request, jsonify, abort
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError, IntegrityError
from json import dumps
from textlink import app, Session
from textlink.models import Entry, Phone, List, PhoneCarrier
from textlink.helpers import get_or_abort, Struct
from textlink.models import lists
from textlink.sources.sendByTwilio import sendSMS
from textlink.sources.emailgateway import *


@app.route('/lists', methods=['POST'])
def create_list():
    """Creates a list with name and returns a JSON object of the list"""
    name = request.form.get('name')
    lst = List(name)
    
    session = Session()
    session.add(lst)
    session.commit()

    print request.url
    return jsonify(data=lst)

@app.route('/lists/', methods=['GET']) #for Testing:
def get_list_index():
    """Returns a list of all Lists in the db, in the form of a JSON object"""
    session = Session()
    return jsonify(lists.get_all(session))

@app.route('/lists/<list_id>/delete', methods=['POST'])
def list_delete(list_id):
    session = Session()
    if not lists.delete(session, list_id):
        abort(404)
    return ""

@app.route('/phones/', methods=['GET']) #for Testing:
def get_all_phones():
    """Returns a list containing all phones in a JSON object"""
    session = Session()
    es = session.query(Phone).all()
    return jsonify(data=es)

@app.route('/phones/<phone_id>/allEntries', methods=['GET']) #for Testing:
def getPhoneEntries(phone_id):
    """Returns a list in JSON form of all entries containing phone_id"""
    session = Session()
    try:
        es = session.query(Entry).filter_by(phone_id=phone_id).all()
    except NoResultFound:
        return none
    else:
        return jsonify(data=es)

@app.route('/phones/<phone_id>', methods=['GET']) #for Testing:
def get_phone(phone_id):
    """Returns a JSON object with the name and number belonging to phone_id"""
    session = Session()
    es = get_or_abort(Phone, phone_id, session)
    return jsonify(data=es)
    
@app.route('/phones/', methods=['GET']) #for Testing:
def get_phones():
    session = Session()
    try:
        es = session.query(Phone).all()
    except NoresultFound:
        return None
    else: 
        es = jsonify(es)
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
        return jsonify(carriers)

    
@app.route('/lists/<list_id>/add', methods=['POST'])
def add_user(list_id):
    """Creates new entry in list_id with number and name. 
    Returns a JSON object of the entry or an error if it alreayd exists"""
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
        print "Phone already exists for this list"
        return jsonify(data=Struct({'entry_id' : entry.entry_id}))
    print dumps({"entry_id" : entry.entry_id})
     
    return dumps({"entry_id" : entry.entry_id})

@app.route('/entries/<entry_id>/delete',methods=['POST'])
def del_entry(entry_id):
    session = Session()
    entry = session.query(Entry).get(entry_id)
    session.delete(entry)
    session.commit()
    #session.query(Entry).filter(Entry.entry_id==entry_id).delete()
    return jsonify(data=entry)

@app.route('/lists/<list_id>/send_email',methods=['POST'])
def send_text(list_id):
    """Sends a text via email to all entries in list_id"""
    sender = request.form.get('sender')
    message = request.form.get('message')
    method = request.form.get('method')
    session = Session()
    lst = session.query(List).get(list_id)
    #attachments = request.form.get('attachments')
    #print message
    if method == "email":
        for ent in lst.entries:
            print dir(ent)
            text_by_email(ent.phone.number, sender, message, ent.phone.textemail)
    else:
        for entry in lst.entries:
            print "sent message"
            sendSMS("AC0955b5ae6e4e14861d9e1f61e7d0680f","a4938640070b8bcaf099093da23676f0", sender, entry.phone.number, message)
    return "success"
        
@app.route('/lists/check_for_bounces',methods=['GET'])
def check_for_bounces():
    checkForBounces()
    return jsonify({})

@app.route('/lists/<list_id>/send_twilio',methods=['POST'])
def send_text_Twilio(list_id):
    """Sends a text via the Twilio API to all entries in list_id"""
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
        sendSMS("sid placeholder","authkey placeholder", sender, entry.phone.number, message)
    return "hello"
