"""
Contains the tests for the apis
"""

from mydiary import app
import unittest


class Test_apis(unittest.TestCase):
    """ This class holds all api tests  """

    #def login_test(self, username, password):

    def test_registration(self):
        tester = app.test_client(self)
        response_reg = tester.post('/auth/signup', \
                    data='{"name": "test user", "email": "email@test.com","password":"testpass"}', \
                    content_type='application/json')
        response_log = tester.post('/auth/login', \
                    data='{"email": "email@test.com","password":"testpass"}', \
                    content_type='application/json')
        #mytoken = response_log.json["access_token"]
        #response_get = tester.get('http://localhost:5000/api/v1/entries/1', \
                    #content_type='application/json'
                    #authorisation=mytoken)
        #self.assertIn('login test data', str(response_get.data))
        self.assertEqual(response_log.status_code, 200)

    def test_login(self):
        tester = app.test_client(self)
        response_reg = tester.post('http://localhost:5000/auth/signup', \
                    data='{"name": "test user", "email": "email@test.com","password":"testpass"}', \
                    content_type='application/json')
        response_log = tester.post('http://localhost:5000/auth/login', \
                    data='{"email": "email@test.com","password":"testpass"}', \
                    content_type='application/json')
        #response_get = tester.get('http://localhost:5000/api/v1/entries/1', \
                    #content_type='application/json')
        #self.assertIn('login test data', str(response_get.data))
        self.assertEqual(response_log.status_code, 200)


    def test_get_one_entry_data(self):
        """ a test for the data returned by the get method and an index """
        tester = app.test_client(self)
        response_reg = tester.post('http://localhost:5000/auth/signup', \
                    data='{"name": "test user", "email": "email@test.com","password":"testpass"}', \
                    content_type='application/json')
        response_log = tester.post('http://localhost:5000/auth/login', \
                    data='{"email": "email@test.com","password":"testpass"}', \
                    content_type='application/json')
        response_add_ent = tester.post('http://localhost:5000/auth/signup', \
                    data='{"entrydata": "entry data for first test"}', \
                    content_type='application/json')
        response_get = tester.get('http://localhost:5000/api/v1/entries/1', \
                    content_type='application/json')
        self.assertIn('entry data for first test', str(response_get.data))
        self.assertEqual(response_get.status_code, 200)

    
    
    # def test_add_new_entry_status_code(self):
    #     """ a test for the status code returned by the post method """
    #     tester = app.test_client(self)
    #     response = tester.post('http://localhost:5000/home/api/v1/entries', \
    #                 data='{"entrydata":"New entry data for post test"}', \
    #                 content_type='application/json')
    #     self.assertEqual(response.status_code, 200)
