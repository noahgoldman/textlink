from json import dumps, JSONEncoder

def is_obj(obj):
    return hasattr(obj, '__dict__') and '_sa_instance_state' in obj.__dict__

def get_dict(obj):
    assert is_obj(obj)

    new_dict = {}
    for key in obj.fields:
        if hasattr(obj, key):
            new_dict[key] = getattr(obj, key)

    return new_dict

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

class ClassTree():

    def __init__(self):
        self.tree = []

    def push(self, obj):
        self.tree.push(type(typ))

    def check(self, obj):
        return type(obj) in self.tree

class TextlinkJSONEncoder(JSONEncoder):

    def default(self, obj):
        self.check_circular = False
        if self.is_model(obj):
            print self.get_types()
            if self.tl_check_circular(obj):
                return None
            model_dict = get_dict(obj)
            self.tl_push(obj)
            return model_dict
        return JSONEncoder.default(self, obj)

    def is_model(self, obj):
        return hasattr(obj, '__dict__') and '_sa_instance_state' in obj.__dict__

    def tl_push(self, obj):
        self.get_types().append(type(obj))

    def tl_check_circular(self, obj):
        return type(obj) in self.get_types()

    def get_types(self):
        try:
            return self.used_types
        except:
            self.used_types = []
            return self.used_types
