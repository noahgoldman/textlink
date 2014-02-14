from functools import wraps
from flask import Response, abort

def API(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        json = f(*args, **kwargs)
        return Response(response=json, mimetype='application/json')
    return wrapper

def get_or_abort(model, obj_id, session, code=404):
    res = session.query(model).get(obj_id)
    return res or abort(code)
