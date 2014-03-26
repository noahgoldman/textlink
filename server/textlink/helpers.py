from flask import abort

def get_or_abort(model, obj_id, session, code=404):
    res = session.query(model).get(obj_id)
    return res or abort(code)
