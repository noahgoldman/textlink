import json

from textlink import Session
from textlink.models import List, Entry, Phone
from tests import TextlinkTestCase

class TestGetPhone(TextlinkTestCase):

    def test_get_phone(self):
        pid = 1
        res = self.app.get('/phones/%d' % pid)

        assert res.status_code == 200 # check that the server return success
        print "The data is " + res.data
        data = json.loads(res.data)

        assert data["data"]['phone_id'] == pid

        # Get the phone object from the database
        session = Session()
        phone = session.query(Phone).get(pid)

        assert phone.name == data["data"]['name']
        assert phone.number == data["data"]['number']
