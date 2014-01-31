from flask import request

from textlink import app, Session
from textlink.models import Entry, Phone, List
from textlink.Obj2JSON import jsonobj

@app.route('/')
def index():
    return "Hello World!"

@app.route('/lists', methods=['POST'])
def create_list():
    name = request.form.get('name')
    print name
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
    
    phone = session.query(Phone).filter_by(number=num).one()
    if not phone:
        phone = Phone(name,num)
        session.add(phone)
        session.commit()
    entry = Entry(list_id, phone.id)
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
