from textlink.models import Key
from textlink.models.keys import create, sign
from textlink.models import users
from tests import TextlinkTestCase

class TestKeys(TextlinkTestCase):
    
    def setUp(self):
        super(TestKeys, self).setUp()
        self.user = users.create(self.session, "derp", "derpfestor")
        self.main_key = create(self.session, self.user)

    def test_create_key(self):
        key = create(self.session, self.user)

        assert key.user_id == self.user.user_id

    def test_key_signature(self):
        msg = "this is a test request"
        hash = sign(self.main_key, msg)
        assert self.main_key.check_signature(msg, hash)
