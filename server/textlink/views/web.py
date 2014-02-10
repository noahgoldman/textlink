from flask import render_template

from textlink import app, Session

@app.route('/')
def index():
    return render_template('base.html')
