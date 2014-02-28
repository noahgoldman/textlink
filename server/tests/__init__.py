import unittest
import os

import fixtures
from textlink import create_db, Session, drop_db, app

class TextlinkTestCase(unittest.TestCase):

    def setUp(self):
        self.init_db()

    def tearDown(self):
        self.drop_db()

    def init_db(self):
        os.environ['TEXTLINK_CONFIG'] = 'TESTING'
        print app.config['DATABASE_URI']
        self.app = app.test_client()
        create_db()
        session = Session()
        fixtures.basic_data(session)

    def drop_db(self):
        drop_db()
