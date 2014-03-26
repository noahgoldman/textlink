from flask.json import JSONEncoder
from inspect import isclass, getmembers
from types import NoneType
from textlink import models

def get_list_type(l):
    typ = reduce(lambda x,y: type(y) if isinstance(y, x) else NoneType, l, object)
    return typ if typ is not NoneType else None

def get_type(obj):
    if isinstance(obj, list):
        return get_list_type(obj)
    return type(obj)

def is_model(obj):
    classes_tuple = getmembers(models, isclass)

    typ = get_type(obj)
    
    for name, cls in classes_tuple:
        if typ == cls:
            return True
    return False

class TextlinkJSONEncoder(JSONEncoder):

    def __init__(self, skipkeys=False, ensure_ascii=True,
            check_circular=True, allow_nan=True, sort_keys=False,
            indent=None, separators=None, encoding='utf-8', default=None):
        super(TextlinkJSONEncoder, self).__init__(skipkeys, ensure_ascii, False,
                allow_nan, sort_keys, indent, separators, encoding, default)

    def default(self, obj):
        try:
            if is_model(obj):
                model_dict = self.get_dict(obj)
                return model_dict
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)

    def get_dict(self, obj):
        new_dict = {}
        for key in obj.fields:
            if hasattr(obj, key):
                self.update_dict(new_dict, obj, key)
        return new_dict

    def update_dict(self, new_dict, obj, key):
        sub_obj = getattr(obj, key)
        if is_model(sub_obj):
            if self.tl_check_key_circular(obj, key):
                return
            self.tl_push(obj, getattr(obj, key))
        new_dict[key] = getattr(obj, key)

    def tl_push(self, parent, obj):
        obj_typ = get_type(obj)
        self.get_types().append(obj_typ)
        self.get_allowed().append((type(parent), obj_typ))

    def tl_check_key_circular(self, obj, key):
        check_obj = getattr(obj, key)
        typ = type(check_obj)
        if isinstance(check_obj, list):
            typ = get_list_type(check_obj)
            assert typ is not None
        return self.tl_check_circular(type(obj), typ)

    def tl_check_circular(self, parent_typ, typ):
        if not isclass(typ):
            typ = type(typ)
        return typ in self.get_types()

    def get_types(self):
        try:
            return self.used_types
        except:
            self.used_types = []
            return self.used_types

    def get_allowed(self):
        try:
            return self.allowed_types
        except:
            self.allowed_types = []
            return self.allowed_types
