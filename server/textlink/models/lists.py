from textlink.models import List

def get_all(session):
    return session.query(List).all()

def delete_list(session, list_id):
    lst = session.query(List).get(list_id)
    if lst is None:
        raise Exception("Failed to find list to delete")

    session.delete(lst)
    session.commit()
