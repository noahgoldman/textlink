from flask import render_template

from textlink import app, Session

from textlink.models import Entry, Phone, List, PhoneCarrier

@app.route('/')
def index():
    session = Session()
    res = session.query(Phone).all()
    # take list ID. display all entries in list 
    return render_template('example.html', x=res)

@app.route('/lists/<list_id>')
def showEntry(list_id):
    session= Session()
    res = session.query(Entry).filter_by(list_id=list_id).all()
    return render_template('showEntries.html', x=res, listid=list_id)
