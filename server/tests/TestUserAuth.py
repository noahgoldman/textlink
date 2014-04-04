from sqlalchemy.exc import IntegrityError

from textlink.models import User
from textlink.models.users import create, auth
from tests import TextlinkTestCase

class TestCreateUser(TextlinkTestCase):

    def setUp(self):
        super(TestCreateUser, self).setUp()
        self.username = "derp"
        self.passw = "derpfestor"
        create(self.session, self.username, self.passw)
        create(self.session, "derpier", "derpfestor2")

    def test_auth_user(self):
        user = auth(self.session, self.username, self.passw)

        assert user is not None
        assert user.name == self.username

    def test_fail_auth(self):
        user = auth(self.session, self.username, "asdf")

        assert user is None
