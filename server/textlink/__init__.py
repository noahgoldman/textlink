from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)

# SQLAlchemy
engine = create_engine('sqlite:///textlink.db', echo=True, convert_unicode=True)
Base = declarative_base()

Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

import views
