import unittest
import json
import inspect
from sqlalchemy import func

from textlink import Session
from textlink.models import Entry, Phone, List
from tests import TextlinkTestCase
from textlink.Obj2JSON import TextlinkJSONEncoder, get_list_type, is_model

# A function for use in these tests to call the json.dumps with the textlink encoder
def dump(obj):
    return json.dumps(obj, cls=TextlinkJSONEncoder)

class TestObj2JSON(TextlinkTestCase):

    def setUp(self):
        super(TestObj2JSON, self).setUp()
        session = Session()
        self.mlist = session.query(List).get(1)
        self.phone = session.query(Phone).get(1)

    def test_get_dict(self):
        dct = dump(self.mlist)
        print dct

        assert 'name' in dct
        assert 'list_id' in dct
    
    def test_get_dict2(self):
        dct = dump(self.phone)

        assert 'number' in dct
        assert 'name' in dct
        assert 'mlist' not in dct

    def test_jsonobj(self):
        json_data = dump(self.mlist)

        lst = json.loads(json_data)
        assert 'name' in lst

    def test_jsonobj2(self):
        json_data = dump(self.phone)

        phone = json.loads(json_data)
        assert 'name' in phone
        assert 'number' in phone

    def test_jsonobj_multiple(self):
        objs = [self.mlist, self.phone]

        json_data = dump(objs)

        lst = json.loads(json_data)

        assert len(lst) is 2

    # Tests for the specific functions of the TextlinkJSONEncoder class

    def test_get_list_type(self):
        lst = ['asdf', 'ahd', 'derp']
        fail_lst = lst + [10]
        fail_lst2 = [10] + lst
        lst2 = list(lst)
        lst2.insert(1, 10)

        assert get_list_type(lst) is str
        assert not get_list_type(fail_lst)
        assert not get_list_type(fail_lst2)
        assert not get_list_type(lst2)

    def test_is_model(self):
        objs = [self.mlist, self.mlist]
        objs2 = [self.phone, self.phone]

        assert is_model(self.mlist)
        assert is_model(objs)
        assert is_model(objs2)
