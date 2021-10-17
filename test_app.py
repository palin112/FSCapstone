import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

from app import create_app
from models import setup_db, Game, Review


#........................ SETUP .................................#


class MyCapstonTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = 'postgres://postgres:password@localhost:5432/capstone'

        setup_db(self.app, self.database_path)

        self.editor_header = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImZrOFF6XzFVd0NhYUdkU2FNNTFoUiJ9.eyJpc3MiOiJodHRwczovL2ZzbmRicmlua2xleS51cy5hdXRoMC5jb20vIiwic3ViIjoiT2tnRXo4MWp1cENETEd5R2FNREZkcGJOcXNvOGFxVGVAY2xpZW50cyIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNjM0NDkzNTgzLCJleHAiOjE2MzQ1Nzk5ODMsImF6cCI6Ik9rZ0V6ODFqdXBDRExHeUdhTURGZHBiTnFzbzhhcVRlIiwic2NvcGUiOiJnZXQ6aXRlbXMgYWRkOml0ZW1zIGVkaXQ6aXRlbXMiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6aXRlbXMiLCJhZGQ6aXRlbXMiLCJlZGl0Oml0ZW1zIl19.W6d7Q6GnED5tq4M6yvmK5GMnxCfuKwKepA4DbLavdKU3l_gtoCIB4i-ZOUrOaXqR4RrGVbrqQkD45svn-oUyy5E2kv3_8BoG1RndKvT-0GbshXBx_S5K9slCAXq93T6JBuLTIzbQUhPm1XFKaVt9e93sev8l32qnkuuYhLiMUq5ha-zz8aAuy9UTRF53Gxkb-EX6EhPB_iJrOJsnQhlPsVAyaJwqphYkYMg4MSfPWf3XCaUAlW_xd8Vgob_dgW1E7e606Yvk6DTuFwXW7EiAFZVYBhGt3v6IWD65DbuknL8dtB4w81rLKabhHcqUPY4Pg3g-aQLawm0cUL98-CjRhw'

        self.reader_header = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImZrOFF6XzFVd0NhYUdkU2FNNTFoUiJ9.eyJpc3MiOiJodHRwczovL2ZzbmRicmlua2xleS51cy5hdXRoMC5jb20vIiwic3ViIjoiT2tnRXo4MWp1cENETEd5R2FNREZkcGJOcXNvOGFxVGVAY2xpZW50cyIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNjM0NDk3NTczLCJleHAiOjE2MzQ1ODM5NzMsImF6cCI6Ik9rZ0V6ODFqdXBDRExHeUdhTURGZHBiTnFzbzhhcVRlIiwic2NvcGUiOiJnZXQ6aXRlbXMiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6aXRlbXMiXX0.m6kkwdP-FVI5ifIoNghE2U2_7MkGQhFheKI-Zrh2QHj3sbIUq6s-LrRpaQ6ZCV0Rk8wTq-a_JsxQode0pB1K0CdBorfR9sNVy2J6PbRZIFYQfDkamAwCLokydOaad2ChCQGnlNROb32TGwWMWmEAxOfAz5T4HAmSbuG-y_-lyHZ6sJUD1FCfwnkyaawAubC75te4c8oxBhjysI2-ikguzdJJiIEGITjgMkoD_X00n3XNKRPD9kl8Vgj3t1022VxY0XbsGmsN3Bc5OYvuZN1s4Rs_1V1kwk592kITDvCZ5ni155NpAt_Gh0Q0fAENasfY-6FZole5c-VgD3ub-aBH6w'

        self.test_game = {'title': 'test game a', 'type': 'Console', 'genre': 'shooter',
                            'category': 'multi-platform', 'description': 'test description'}

        self.test_game_patch = {'title': 'patched game a', 'type': 'Console', 'genre': 'shooter',
                            'category': 'multi-platform', 'description': 'test description'}

        self.test_review = {'game_id': 1, 'rating': 1, 'reviewer': 'unittest', 'review': 'under review'}

        self.test_review_patch = {'game_id': 1, 'rating': 10, 'reviewer': 'patched', 'review': 'patched review'}

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

    def tearDown(self):
        pass


#........................ TESTS .................................#

#........................ GET GAMES..............................#
    def test_get_games(self):
        res = self.client().get('/games', headers={'Authorization': 'Bearer ' + self.editor_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['games']))


    def test_401_get_games_no_header(self):
        res = self.client().get('/games')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], 'Authentication Error')
        self.assertFalse(data['success'])

#........................ GET REVIEWS ..............................#
    def test_get_review(self):
        res = self.client().get('/review/1', headers={'Authorization': 'Bearer ' + self.editor_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['reviews'][0]['game_id'], 1)
        self.assertTrue(data['success'])

    def test_get_review_game_missing(self):
        res = self.client().get('/review/999999', headers={'Authorization': 'Bearer ' + self.editor_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'Requested resource not found.')
        self.assertFalse(data['success'])

#........................ ADD A GAME..............................#
    def test_post_game(self):
        res = self.client().post('/games', json=self.test_game,headers={'Authorization': 'Bearer ' + self.editor_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['added_game']['category'], 'multi-platform')

    def test_post_game_no_authorization(self):
        res = self.client().post('/games', json=self.test_game)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], 'Authentication Error')
        self.assertFalse(data['success'])

#........................ ADD A REVIEW..............................#
    def test_post_review(self):
        res = self.client().post('/review', json=self.test_review,headers={'Authorization': 'Bearer ' + self.editor_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['added_review']['rating'], 1)

    def test_post_review_not_authorized(self):
        res = self.client().post('/review', json=self.test_review,headers={'Authorization': 'Bearer ' + self.reader_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['authentication_error_message']['code'], 'permission not found')


#........................ PATCH A GAME..............................#
    def test_patch_game(self):
        res = self.client().patch('/games/7',json=self.test_game_patch, headers={'Authorization': 'Bearer ' + self.editor_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_patch_game_does_not_exist(self):
        res = self.client().patch('/games/9999', headers={'Authorization': 'Bearer ' + self.editor_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

#........................ PATCH A REVIEW..............................#
    def test_patch_review(self):
        res = self.client().patch('/review/3',json=self.test_review_patch, headers={'Authorization': 'Bearer ' + self.editor_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_patch_review_does_not_exist(self):
        res = self.client().patch('/review/9999', headers={'Authorization': 'Bearer ' + self.editor_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])


#........................ DELETE A GAME..............................#
    def test_delete_game(self):
        res = self.client().delete('/games/10', headers={'Authorization': 'Bearer ' + self.editor_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_delete_game_no_auth_header(self):
        res = self.client().delete('/games/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], 'Authentication Error')
        self.assertFalse(data['success'])

#........................ DELETE A REVIEW..............................#
    def test_delete_review(self):
        res = self.client().delete('/review/3', headers={'Authorization': 'Bearer ' + self.editor_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_delete_review_no_auth_header(self):
        res = self.client().delete('/review/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], 'Authentication Error')
        self.assertFalse(data['success'])




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
