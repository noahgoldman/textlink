import unittest
import json

from textlink import app, create_db, Session, drop_db
from textlink.models import List, Entry, Phone
import fixtures

class TestCreateList(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        create_db()
        session = Session()
        fixtures.basic_data(session)

    def test_create_list(self):
        list_name = "TestList"
        res = self.app.post('/lists', data=dict(
            name=list_name,
        ))

        res_list = json.loads(res.data)
        assert res_list["name"] == list_name

        # Check against the database
        session = Session()
        data_list = session.query(List).get(res_list["list_id"])
        assert data_list.name == list_name

    def test_create_list2(self):
        list_name2 = "TestList2"
        res = self.app.post('/lists', data=dict(
            name=list_name2,
        ))

        res_list = json.loads(res.data)
        assert res_list["name"] == list_name2

        # Check against the database
        session = Session()
        data_list = session.query(List).get(res_list["list_id"])
        assert data_list.name == list_name2

    def tearDown(self):
        drop_db()
