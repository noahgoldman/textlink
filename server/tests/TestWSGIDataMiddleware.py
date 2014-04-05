from flask import request

from tests import TextlinkTestCase

class TestWSGIDataMiddleware(TextlinkTestCase):

    def test_get_post_data(self):
        with self.app as client:
            res = client.post('/', data=dict(
                item1='derp',
                item2='ohair',
            ), follow_redirects=False)
            data = request.environ['req_data']
            assert 'derp' in data
            assert 'item2' in data

    def test_get_get_data(self):
        with self.app as client:
            res = client.get('/')
            data = request.environ['req_data']
            assert not data
