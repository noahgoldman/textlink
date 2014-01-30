from json import dumps

def is_obj(obj):
    return hasattr(obj, '__dict__') and '_sa_instance_state' in obj.__dict__

def get_dict(obj):
    assert is_obj(obj)

    old_dict = obj.__dict__
    new_dict = {}
    for key in old_dict:
        print key
        if key in obj.fields:
            new_dict[key] = old_dict[key] 

    return new_dict

def jsonobj(obj):
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
