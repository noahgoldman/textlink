from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
import bcrypt

from textlink.models import User

def create(session, name, password):
    user = User(name, password)
    session.add(user)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise

def auth(session, name, password):
    user = session.query(User).filter(User.name == name).one()
    return user if user.check_pass(password) else None
