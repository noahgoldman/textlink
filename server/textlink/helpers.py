from flask import abort

def get_or_abort(model, obj_id, session, code=404):
    res = session.query(model).get(obj_id)
    return res or abort(code)


class Struct(object):
    def __init__(self, adict):
        """Convert a dictionary to a class

        @param :adict Dictionary
        """
        self.__dict__.update(adict)
        for k, v in adict.items():
            if isinstance(v, dict):
                self.__dict__[k] = Struct(v)
