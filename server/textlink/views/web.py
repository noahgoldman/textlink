from flask import render_template

from textlink import app, Session

from textlink.models import Entry, Phone, List, PhoneCarrier

@app.route('/')
def index():
    session= Session()
    qResults = session.query(Phone).all()
    # take list ID. display all entries in list 
    return render_template('example.html', x=qResults)

@app.route('/lists/<list_id>')
def showEntry(list_id):
    session= Session()
    qResults = session.query(Entry).filter_by(list_id=list_id).all()
    return render_template('showEntries.html', x=qResults, listid=list_id)


