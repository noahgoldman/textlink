import json

from textlink import Session
from textlink.models import List, Entry, Phone
from tests import TextlinkTestCase

class TestCreateList(TextlinkTestCase):

    def test_create_list(self):
        list_name = "TestList"
        res = self.app.post('/lists', data=dict(
            name=list_name,
        ))

        res_list = json.loads(res.data)
        assert res_list["data"]["name"] == list_name

        # Check against the database
        session = Session()
        data_list = session.query(List).get(res_list["data"]["list_id"])
        assert data_list.name == list_name

    def test_create_list2(self):
        list_name2 = "TestList2"
        res = self.app.post('/lists', data=dict(
            name=list_name2,
        ))

        res_list = json.loads(res.data)
        assert res_list["data"]["name"] == list_name2

        # Check against the database
        session = Session()
        data_list = session.query(List).get(res_list["data"]["list_id"])
        assert data_list.name == list_name2

    def test_create_existing_list(self):
        list_name = "TestRunner" # A name in fixtures.py
        res = self.app.post('/lists', data=dict(
            name=list_name,
        ))

        assert res.status_code == 200
