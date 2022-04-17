import os
import warnings
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
import string
import random
from app import create_app
from models import setup_db, Actor, Movie

import http.client


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""
    CASTING_ASSISTANT_TOKEN = ""
    CASTING_DIRECTOR_TOKEN = ""
    EXECUTIVE_DIRECTOR_TOKEN = ""

    
    def init_tokens(self):
        
        conn = http.client.HTTPSConnection("dev-i2ernxx1.us.auth0.com")
        '''
        payload = 'client_id=cdqFbHMUDc8oNQwb3WPGGLCJF1tfGMv5&username=casting_assistant%40castingagency.com&audience=casting-agency&grant_type=password&password=yXiR1sXn1ThO&client_secret=RiuGdWH6P5e_LF4uPZjqswqBCEE4DbDGEfrCANDlhD6KOj78C4Z4OpUpnJlzBLag'
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'did=s%3Av0%3Add30a500-bc24-11ec-90de-a7124a4cbecb.7ZSn0b4ddbD4EfZ8hMyi8An9T6ZChkVXNc5FsQYGzMY; did_compat=s%3Av0%3Add30a500-bc24-11ec-90de-a7124a4cbecb.7ZSn0b4ddbD4EfZ8hMyi8An9T6ZChkVXNc5FsQYGzMY'
        }
        conn.request("POST", "/oauth/token", payload, headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data.decode())
        self.CASTING_ASSISTANT_TOKEN = data['access_token']

        payload = 'client_id=cdqFbHMUDc8oNQwb3WPGGLCJF1tfGMv5&username=casting_director%40castingagency.com&audience=casting-agency&grant_type=password&password=yXiR1sXn1ThO&client_secret=RiuGdWH6P5e_LF4uPZjqswqBCEE4DbDGEfrCANDlhD6KOj78C4Z4OpUpnJlzBLag'
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'did=s%3Av0%3Add30a500-bc24-11ec-90de-a7124a4cbecb.7ZSn0b4ddbD4EfZ8hMyi8An9T6ZChkVXNc5FsQYGzMY; did_compat=s%3Av0%3Add30a500-bc24-11ec-90de-a7124a4cbecb.7ZSn0b4ddbD4EfZ8hMyi8An9T6ZChkVXNc5FsQYGzMY'
        }
        conn.request("POST", "/oauth/token", payload, headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data.decode())
        self.CASTING_DIRECTOR_TOKEN = data['access_token']
        '''

        payload = 'client_id=cdqFbHMUDc8oNQwb3WPGGLCJF1tfGMv5&username=executive_producer%40castingagency.com&audience=casting-agency&grant_type=password&password=yXiR1sXn1ThO&client_secret=RiuGdWH6P5e_LF4uPZjqswqBCEE4DbDGEfrCANDlhD6KOj78C4Z4OpUpnJlzBLag'
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'did=s%3Av0%3Add30a500-bc24-11ec-90de-a7124a4cbecb.7ZSn0b4ddbD4EfZ8hMyi8An9T6ZChkVXNc5FsQYGzMY; did_compat=s%3Av0%3Add30a500-bc24-11ec-90de-a7124a4cbecb.7ZSn0b4ddbD4EfZ8hMyi8An9T6ZChkVXNc5FsQYGzMY'
        }
        conn.request("POST", "/oauth/token", payload, headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data.decode())
        self.EXECUTIVE_DIRECTOR_TOKEN = data['access_token']


    def setUp(self):
        warnings.simplefilter('ignore', category=ResourceWarning)
        warnings.simplefilter('ignore', category=DeprecationWarning)
        self.init_tokens()

        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_success_get_actors(self):
        res = self.client().get("/api/v1/actors", headers={'Authorization': 'Bearer ' + self.EXECUTIVE_DIRECTOR_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["actors"])
        self.assertTrue(len(data["actors"]))

    def test_success_create_actors(self):
        json_dict = {
            "firstName": "Emma",
            "lastName": "Watson",
            "gender": "Female",
            "dateOfBirth": "1987-01-01",
            "age": 32
        }

        res = self.client().post("/api/v1/actors", json = json_dict, headers={'Authorization': 'Bearer ' + self.EXECUTIVE_DIRECTOR_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["result"], "Actor created successfuly.")

    def test_success_delete_actor(self):

        res = self.client().get("/api/v1/actors", headers={'Authorization': 'Bearer ' + self.EXECUTIVE_DIRECTOR_TOKEN})
        data = json.loads(res.data)

        for actor in data['actors']:
            if actor['firstName'] == 'Emma':
                id = actor['id']

        res = self.client().delete("/api/v1/actors/" + str(id), headers={'Authorization': 'Bearer ' + self.EXECUTIVE_DIRECTOR_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["result"], "Actor deleted successfuly.")

    
    def test_401_get_actors(self):
        res = self.client().get("/api/v1/actors", headers={'Authorization': 'Bearer '})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_401_create_actors(self):
        json_dict = {
            "firstName": "Emma",
            "lastName": "Watson",
            "gender": "Female",
            "dateOfBirth": "1987-01-01",
            "age": 32
        }

        res = self.client().post("/api/v1/actors", json = json_dict, headers={'Authorization': 'Bearer '})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_401_delete_actor(self):

        res = self.client().delete("/api/v1/actors/1", headers={'Authorization': 'Bearer '})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    
    def test_success_get_movies(self):
        res = self.client().get("/api/v1/movies", headers={'Authorization': 'Bearer ' + self.EXECUTIVE_DIRECTOR_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["movies"])
        self.assertTrue(len(data["movies"]))

    def test_success_create_movies(self):
        json_dict = {
            "title": "Harry Potter",
            "genre": "Fantasy",
            "rating": "5",
            "releaseDate": "2020-01-01"
        }

        res = self.client().post("/api/v1/movies", json = json_dict, headers={'Authorization': 'Bearer ' + self.EXECUTIVE_DIRECTOR_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["result"], "Movie created successfuly.")

    def test_success_delete_movie(self):

        res = self.client().get("/api/v1/movies", headers={'Authorization': 'Bearer ' + self.EXECUTIVE_DIRECTOR_TOKEN})
        data = json.loads(res.data)

        for actor in data['movies']:
            if actor['title'] == 'Harry Potter':
                id = actor['id']

        res = self.client().delete("/api/v1/movies/" + str(id), headers={'Authorization': 'Bearer ' + self.EXECUTIVE_DIRECTOR_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["result"], "Movie deleted successfuly.")

    
    def test_401_get_movies(self):
        res = self.client().get("/api/v1/movies", headers={'Authorization': 'Bearer '})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_401_create_movie(self):
        json_dict = {
            "title": "Harry Potter",
            "genre": "Fantasy",
            "rating": "5",
            "releaseDate": "2020-01-01"
        }

        res = self.client().post("/api/v1/movies", json = json_dict, headers={'Authorization': 'Bearer '})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_401_delete_movie(self):

        res = self.client().delete("/api/v1/movies/1", headers={'Authorization': 'Bearer '})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()