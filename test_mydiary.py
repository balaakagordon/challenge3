"""
Contains the tests for the apis
"""

from ..app import app
import unittest


class Test_apis(unittest.TestCase):
    """ This class holds all api tests  """
    def __init__(self):
        app.config['TESTING'] = True

    def test_get_one_entry_data(self):
        """ a test for the data returned by the get method and an index """
        tester = app.test_client(self)
        response = tester.get('http://localhost:5000/api/v1/entries/2', \
                    content_type='application/json')
        self.assertIn('this is my second entry', str(response.data))
