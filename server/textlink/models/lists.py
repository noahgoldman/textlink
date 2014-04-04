from textlink.models import List

def get_all(session):
    return session.query(List).all()

def delete(session, list_id):
    lst = session.query(List).get(list_id)
    if lst is None:
        return False

    session.delete(lst)
    session.commit()
    return True
