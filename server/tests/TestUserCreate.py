from sqlalchemy.exc import IntegrityError

from textlink.models import User
from textlink.models.users import create
from tests import TextlinkTestCase

class TestCreateUser(TextlinkTestCase):

    def test_create_user(self):
        create(self.session, "derp", "derpfestor")

        assert self.session.query(User).count() is 1

    def test_create_two_users(self):
        create(self.session, "derp", "derpfestor")
        create(self.session, "derpier", "derpfestor2")

        assert self.session.query(User).count() is 2

    def test_create_duplicate_user(self):
        create(self.session, "derp", "derpfestor")
        try:
            create(self.session, "derp", "derpfestor")
        except IntegrityError:
            assert True
        else:
            assert False

        assert self.session.query(User).count() is 1
