from json import dumps, JSONEncoder
from inspect import isclass
from types import NoneType

def jsonobj(obj, class_tree = None):
    json = None
    if isinstance(obj, list):
        new_list = []
        for ob in obj:
            new_list.append(get_dict(ob))
        json = dumps(new_list)
    elif is_obj(obj):
        new_dict = get_dict(obj)
        json = dumps(new_dict)

    return json

def get_list_type(l):
    typ = reduce(lambda x,y: type(y) if isinstance(y, x) else NoneType, l, object)
    return typ if typ is not NoneType else None

class TextlinkJSONEncoder(JSONEncoder):

    def __init__(self, skipkeys=False, ensure_ascii=True,
            check_circular=True, allow_nan=True, sort_keys=False,
            indent=None, separators=None, encoding='utf-8', default=None):
        super(TextlinkJSONEncoder, self).__init__(skipkeys, ensure_ascii, False,
                allow_nan, sort_keys, indent, separators, encoding, default)

    def default(self, obj):
        if self.is_model(obj):
            #if self.tl_check_circular(obj):
            #    return None
            model_dict = self.get_dict(obj)
            self.tl_push(obj)
            return model_dict
        return JSONEncoder.default(self, obj)

    def get_dict(self, obj):
        new_dict = {}
        for key in obj.fields:
            if hasattr(obj, key):
                if self.tl_check_key_circular(obj, key):
                    print obj
                else:
                    new_dict[key] = getattr(obj, key)

        return new_dict

    def is_model(self, obj):
        return hasattr(obj, '__dict__') and '_sa_instance_state' in obj.__dict__

    def tl_push(self, obj):
        self.get_types().append(type(obj))

    def tl_check_key_circular(self, obj, key):
        check_obj = getattr(obj, key)
        typ = type(check_obj)
        if isinstance(check_obj, list):
            typ = get_list_type(check_obj)
            assert typ is not None
        return self.tl_check_circular(typ)

    def tl_check_circular(self, typ):
        if not isclass(typ):
            typ = type(typ)
        return typ in self.get_types()

    def get_types(self):
        try:
            return self.used_types
        except:
            self.used_types = []
            return self.used_types
