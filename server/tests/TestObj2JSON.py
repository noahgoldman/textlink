import unittest
import json
from textlink.models import Entry, Phone, List
from textlink import Obj2JSON

class TestObj2JSON(unittest.TestCase):

    def setUp(self):
        self.mlist = List("derp")
        self.phone = Phone('derp', '12312')

    def test_get_dict(self):
        dct = Obj2JSON.get_dict(self.mlist)

        assert len(dct) is 1
        assert 'name' in dct
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
