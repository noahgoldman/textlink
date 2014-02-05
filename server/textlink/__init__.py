from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from textlink.config import load_config

app = Flask(__name__)
load_config(app)

# SQLAlchemy
engine = create_engine(app.config['DATABASE_URI'], echo=True, convert_unicode=True)
Base = declarative_base()

Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

import views

def create_db():
    Base.metadata.create_all(bind=engine)

def drop_db():
    Base.metadata.drop_all(bind=engine)
