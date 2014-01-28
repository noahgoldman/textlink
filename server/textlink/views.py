from flask import request

from textlink import app, Session
from textlink.models import Number, Phone, List

@app.route('/')
def index():
    return "Hello World!"

@app.route('/lists', methods=['POST'])
def create_list():
    name = request.args.get('name')
    print name
    lst = List(name)
    
    session = Session()
    session.add(lst)
    session.commit()

    return str(lst.id)
