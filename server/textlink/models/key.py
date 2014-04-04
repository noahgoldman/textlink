from textlink.models import Key

def create(session, user):
    key = Key(user)
    session.add(key)
    session.commit()
