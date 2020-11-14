import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['categories']), 6)

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        
        res= self.client().get('/questions?page=100')        
        self.assertEqual(res.status_code, 400)

    def test_delete_question(self):
        res = self.client().delete('/questions/6')
        self.assertEqual(res.status_code, 200)

        res = self.client().delete('questions/100')
        self.assertEqual(res.status_code,404)

    def test_add_question(self):
        res= self.client().post('/questions', json = {'question': 'Test', 'answer': 'test', 'category': 1, 'difficulty': 2})
        self.assertEqual(res.status_code, 200)

        res= self.client().post('/questions', json = {'question': ''})
        self.assertEqual(res.status_code, 400)
    
    def test_search_question(self):
        res= self.client().post('/questions', json = {'search_term': 'hi'})
        data = json.loads(res.data)
        self.assertEqual(len(data), 13)

        res= self.client().post('/questions', json = {'search_term': 'Something that doesnt exist'})
        data = json.loads(res.data)
        self.assertEqual(len(data), 0)

    def test_get_questions_from_category(self):
        res= self.client().get('/categories/6/questions')
        data = json.loads(res.data)
        self.assertGreater(len(data['questions']), 0)

        res= self.client().get('/categories/100/questions')
        data = json.loads(res.data)
        self.assertEqual(data['error'], 404)

    def test_next_question(self):
        res= self.client().post('/quiz', json = {'category': 2, 'previous_questions': [16]})
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertGreater(len(data['question']), 0)

        res = self.client().get('/quiz')
        self.assertEqual(res.status_code, 405)

    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()