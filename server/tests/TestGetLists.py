import json

from textlink.models.lists import get_all
from tests import TextlinkTestCase

class TestGetAllLists(TextlinkTestCase):

    def test_get_all_lists(self):
        lists = get_all(self.session)

        assert len(lists) is 2
        
        for lst in lists:
            assert len(lst.entries) > 0
