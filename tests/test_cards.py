import unittest
from flask import Blueprint
from unittest.mock import patch, MagicMock
from sqlalchemy.orm.exc import NoResultFound
from ..models import User, Cards, Card_type
from .. import create_app, db

class TestCards(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Initialize the app
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

    @classmethod
    def tearDownClass(cls):
        cls.app_context.pop()

    def test_questions_endpoint(self):
        response = self.client.get('/api/tarjeta/questions')
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], 'Preguntas encontradas')
        self.assertIn('data', data)
        self.assertIsInstance(data['data'], list)
        self.assertGreater(len(data['data']), 0)

    def test_tarjeta_missing_idCliente(self):
        response = self.client.post('/api/tarjeta', json={})
        self.assertEqual(response.status_code, 400)
        data = response.json
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'No se proporcionó el id del cliente')


if __name__ == '__main__':
    unittest.main()
