import unittest
import json
from sqlalchemy import func

from textlink.models import Entry, Phone, List
from textlink import Obj2JSON, Session
from tests import TextlinkTestCase
from textlink.Obj2JSON import TextlinkJSONEncoder

class TestObj2JSON(TextlinkTestCase):

    def setUp(self):
        super(TestObj2JSON, self).setUp()
        session = Session()
        self.mlist = session.query(List).get(1)
        self.phone = session.query(Phone).get(1)

    def test_get_dict(self):
        print dir(self.mlist)
        dct = Obj2JSON.get_dict(self.mlist)

        #print Obj2JSON.jsonobj(self.mlist)
        #assert len(dct) is 2
        assert 'name' in dct
        assert 'list_id' in dct
        assert 'id' not in dct
    
    def test_get_dict2(self):
        dct = Obj2JSON.get_dict(self.phone)

        assert 'number' in dct
        assert 'name' in dct
        assert 'mlist' not in dct

    def test_is_obj(self):
        l1 = []
        l1.append('derp')
        l1.append('derpier')
        
        assert not Obj2JSON.is_obj(l1)
        assert Obj2JSON.is_obj(self.mlist)

    def test_jsonobj(self):
        json_data = Obj2JSON.jsonobj(self.mlist)

        lst = json.loads(json_data)
        assert 'name' in lst

    def test_jsonobj2(self):
        json_data = Obj2JSON.jsonobj(self.phone)

        phone = json.loads(json_data)
        assert 'name' in phone
        assert 'number' in phone

    def test_jsonobj_multiple(self):
        objs = [self.mlist, self.phone]

        json_data = Obj2JSON.jsonobj(objs)

        lst = json.loads(json_data)

        assert len(lst) is 2

    # Tests for the specific functions of the TextlinkJSONEncoder class

    def test_get_list_type(self):
        lst = ['asdf', 'ahd', 'derp']
        fail_lst = lst + [10]
        fail_lst2 = [10] + lst
        lst2 = list(lst)
        lst2.insert(1, 10)

        assert TextlinkJSONEncoder.get_list_type(lst) is str
        assert not TextlinkJSONEncoder.get_list_type(fail_lst)
        assert not TextlinkJSONEncoder.get_list_type(fail_lst2)
        assert not TextlinkJSONEncoder.get_list_type(lst2)
