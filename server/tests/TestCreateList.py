import unittest
import json

from textlink import app, create_db
from textlink.models import List, Entry, Phone

class TestCreateList(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        create_db()

    def test_create_list(self):
        list_name = "TestList"
        res = self.app.post('/lists', data=dict(
            name=list_name,
        ))

        res_list = json.loads(res.data)
        assert res_list["name"] == list_name

    def tearDown(self):
        pass
