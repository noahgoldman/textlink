import json

from textlink.models.lists import get_all, delete_list
from tests import TextlinkTestCase

class TestDeleteList(TextlinkTestCase):

    def test_delete_list(self):
        assert len(get_all(self.session)) is 2

        delete_list(self.session, 1)

        assert len(get_all(self.session)) is 1

    def test_delete_list_fail(self):
        try:
            delete_list(self.session, 10)
        except Exception:
            assert True
        else:
            assert False
