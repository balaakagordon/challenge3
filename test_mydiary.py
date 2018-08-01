"""
Contains the tests for the apis
"""
from flask import json
import unittest

from mydiary import app


class Test_apis(unittest.TestCase):
    """ This class holds all api tests  """

    #def login_test(self, username, password):

    def test_registration(self):
        tester = app.test_client(self)
        response_reg = tester.post('/auth/signup', data=json.dumps('{"name": "test user", "email": "email@test.com", "password":"testpass"}'), content_type='application/json')
        self.assertEqual(response_reg.status_code, 201)

    def test_login(self):
        tester = app.test_client(self)
        response_reg = tester.post('/auth/signup', \
                        data=json.dumps('{"name": "test user",\
                        "email": "email@test.com","password":"testpass"}'), \
                        content_type='application/json')
        response_log = tester.post('/auth/login', \
                        data=json.dumps('{"email": "email@test.com",\
                        "password":"testpass"}'), \
                        content_type='application/json')
        self.assertIn('access_token', str(response_log.data))
        self.assertEqual(response_log.status_code, 200)

    def test_add_new_entry(self):
        """ a test for the status code returned by the post method """
        tester = app.test_client(self)
        response_reg = tester.post('/auth/signup',\
                        data=json.dumps('{"name": "test user",\
                        "email": "email@test.com",\
                        "password":"testpass"}'),\
                        content_type='application/json')
        response_log = tester.post('/auth/login',\
                        data=json.dumps('{"email": "email@test.com",\
                        "password":"testpass"}'),\
                        content_type='application/json')
        mytoken = response_log.data["access_token"]
        response_add_ent = tester.post('/api/v1/entries',\
                        data=json.dumps('{"entrydata":"Test for adding a new entry",\
                        "entrytitle": "New entry test"}'),\
                        content_type='application/json',\
                        authorization= 'Bearer ' + str(mytoken))
        response_add_ent_err = tester.post('/api/v1/entries',\
                        data='{"entrydata":"Test for adding a new entry",\
                        "entrytitle": "New entry test"}',\
                        content_type='application/json',\
                        authorization= 'Bearer ' + str(mytoken))
        response_add_ent_err1 = tester.post('/api/v1/entries',\
                        data=json.dumps('{"data":"Test for adding a new entry",\
                        "entrytitle": "New entry test"}'),\
                        content_type='application/json',\
                        authorization= 'Bearer ' + str(mytoken))
        response_add_ent_err2 = tester.post('/api/v1/entries',\
                        data=json.dumps('{"entrydata":"Test for adding a new entry",\
                        "title": "New entry test"}'),\
                        content_type='application/json',\
                        authorization= 'Bearer ' + str(mytoken))
        response_add_ent_repeat = tester.post('/api/v1/entries',\
                        data=json.dumps('{"entrydata":"Test for adding a new entry",\
                        "entrytitle": "New entry test"}'),\
                        content_type='application/json',\
                        authorization= 'Bearer ' + str(mytoken))                        
        self.assertEqual(response_add_ent.status_code, 201)
        self.assertEqual(response_add_ent_err.status_code, 401)
        self.assertIn('please input json data', str(response_add_ent_err.data))
        self.assertEqual(response_add_ent_err1.status_code, 400)
        self.assertIn('Diary entry field cannot be left blank', str(response_add_ent_err1.data))
        self.assertEqual(response_add_ent_err2.status_code, 400)
        self.assertIn('Diary entry title cannot be left blank', str(response_add_ent_err2.data))
        self.assertEqual(response_add_ent_repeat.status_code, 400)
        self.assertIn('Entry already exists', str(response_add_ent_repeat.data))

    def test_get_one_entry_data(self):
        """ a test for the data returned by the get method and an index """
        tester = app.test_client(self)
        response_reg = tester.post('/auth/signup',\
                        data=json.dumps('{"name": "test user",\
                        "email": "email@test.com","password":"testpass"}'),\
                        content_type='application/json')
        response_log = tester.post('/auth/login',\
                        data=json.dumps('{"email": "email@test.com",\
                        "password":"testpass"}'),\
                        content_type='application/json')
        mytoken = response_log.data["access_token"]
        response_add_ent = tester.post('/api/v1/entries',\
                        data=json.dumps('{"entrydata": "test getting one entry",\
                        "entrytitle": "test method"}'),\
                        content_type='application/json',\
                        authorization= 'Bearer ' + str(mytoken))
        response_get = tester.get('/api/v1/entries/1',\
                        content_type='application/json', \
                        authorization= 'Bearer ' + str(mytoken))
        self.assertIn('test getting one entry', str(response_get.data))
        self.assertEqual(response_get.status_code, 200)

    def test_get_all_entries_data(self):
        """ a test for the data returned by the get method and no entry index """
        tester = app.test_client(self)
        response = tester.get('http://localhost:5000/home/api/v1/entries', \
                    content_type='application/json')
        self.assertIn('this is my first entry', str(response.data))
        self.assertIn('this is my second entry', str(response.data))
    
    
