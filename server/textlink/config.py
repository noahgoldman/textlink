import os
from textlink.Obj2JSON import TextlinkJSONEncoder

def get_class_name(obj):
    return obj.__name__

def load_config(app):
    cfg = os.getenv('TEXTLINK_CONFIG', "")
    obj = "textlink.config."

    if cfg == 'TESTING':
        obj += get_class_name(Testing) 
    else:
        obj += get_class_name(Config)

    app.config.from_object(obj)
    app.json_encoder = TextlinkJSONEncoder

class Config(object):
    DEBUG = True
    TESTING = True
    DATABASE_URI = 'sqlite:///textlink.db'

class Testing(Config):
    DEBUG = True
    TESTING = True
    DATABASE_URI = 'sqlite:///'
