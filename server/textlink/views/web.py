from flask import render_template, request

from textlink import app, Session

from textlink.models import Entry, Phone, List, PhoneCarrier
from textlink.models import lists

@app.route('/')
def index():
    session = Session()
    res = session.query(Phone).all()
    # take list ID. display all entries in list 
    return render_template('example.html', x=res)

@app.route('/web/lists/<list_id>')
def list_detail(list_id):
    print request.url
    session= Session()
    res = session.query(Entry).filter_by(list_id=list_id).all()
    return render_template('showEntries.html', x=res, listid=list_id)

@app.route('/web/lists/')
def list_index():
    session = Session()
    lsts = lists.get_all(session)
    return render_template('list_index.html', lists=lsts)
