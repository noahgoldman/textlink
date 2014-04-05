from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from textlink.config import load_config
from textlink.models import Base
from textlink.middleware import WSGISaveData

app = Flask(__name__)
app.wsgi_app = WSGISaveData(app.wsgi_app)
load_config(app)
engine = create_engine(app.config['DATABASE_URI'], echo=True, convert_unicode=True)

Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

from views import api, web

def create_db():
    Base.metadata.create_all(bind=engine)

def drop_db():
    Base.metadata.drop_all(bind=engine)
