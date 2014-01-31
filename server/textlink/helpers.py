from functools import wraps
from flask import Response

def API(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        json = f(*args, **kwargs)
        return Response(response=json, mimetype='application/json')
    return wrapper
