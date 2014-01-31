from flask import request
from sqlalchemy.orm.exc import NoResultFound
from textlink import app, Session
from textlink.models import Entry, Phone, List
from textlink.Obj2JSON import jsonobj
from textlink.helpers import API
from textlink.sources.sendByTwilio import sendSMS

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
    
@app.route('/lists/<list_id>', methods=['GET']) #for Testing:
def list_list(list_id):
    session = Session()
    es = session.query(Entry).filter_by(mlist=list_id).all()
    es = jsonobj(es)
    return es

@app.route('/lists/<list_id>/add', methods=['POST']) #for Testing:
def add_user(list_id):
    #Need to not allow multiples.
    num = request.form.get('number')
    name = request.form.get('name')
    session = Session()
    
    try:
        phone = session.query(Phone).filter_by(number=num).one()
    except NoResultFound:
        phone = Phone(name,num)
        session.add(phone)
        session.commit()
    entry = Entry(list_id, phone.phone_id)
    session.add(entry)
    session.commit()
    return jsonobj(entry)

@app.route('/lists/<list_id>',methods=['POST'])
def send_text():
    name = request.form.get('name')
    sender = request.form.get('sender')
    print sender
    message = request.form.get('message')
    lst = List(name)
    #attachments = request.form.get('attachments')
    print message
    for phone in lst.phones:
        text_by_email(phone.number, sender, message, phone.textemail)

@app.route('/lists/<list_id>/send',methods=['POST'])
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
