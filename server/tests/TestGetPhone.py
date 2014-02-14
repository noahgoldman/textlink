import json

from textlink import Session
from textlink.models import List, Entry, Phone
from tests import TextlinkTestCase

class TestGetPhone(TextlinkTestCase):

    def test_get_phone(self):
        pid = 1
        res = self.app.get('/phones/%d' % pid)

        assert res.status_code == 200 # check that the server return success
        data = json.loads(res.data)

        assert data['phone_id'] == pid

        # Get the phone object from the database
        session = Session()
        phone = session.query(Phone).get(pid)

        assert phone.name == data['name']
        assert phone.number == data['number']
