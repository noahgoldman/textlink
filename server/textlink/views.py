from flask import request

from textlink import app, Session
from textlink.models import Number, Phone, List
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
