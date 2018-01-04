# -*- coding: utf-8 -*-
"""
    Kiwiland Trains Tests
    ~~~~~~~~~~~~
    Tests the trains application.
"""

import unittest,json
from trains import app
from trains.trainsApp import getOutput

class TrainsTestCase(unittest.TestCase):
    
    def setUp(self):
        app.testing = True
        self.app = app.test_client()
              
    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
            
    def test_getOutput(self):
        with app.app_context():
            with app.test_request_context(): 
                rv = getOutput('1', ['A','E','B','C','D'],'','','')
                res = json.loads(rv.data)
                self.assertEqual(res['result'], 22)
                rv = getOutput('1', ['A','E','D'],'','','')
                res = json.loads(rv.data)
                assert 'route does not exist' in res['result']
                rv = getOutput('2', ['C','C'],3,'','1')
                res = json.loads(rv.data)
                self.assertEqual(res['result'][0], 2)
                rv = getOutput('2', ['C','C','D'],'','','')
                res = json.loads(rv.data)
                assert 'not possible' in res['result']
                rv = getOutput('2', ['A','C'], 4 ,'','2')
                res = json.loads(rv.data)
                self.assertEqual(res['result'][0], 3)
                rv = getOutput('2', ['A','C','D'],'','','')
                res = json.loads(rv.data)
                assert 'not possible' in res['result']
                rv = getOutput('3', ['A','C'],'','','')
                res = json.loads(rv.data)
                self.assertEqual(res['result'][0], 9)
                rv = getOutput('4', ['C','C'],'',30,'1')
                res = json.loads(rv.data)
                self.assertEqual(res['result'][0], 7)

if __name__ == '__main__':
    unittest.main()