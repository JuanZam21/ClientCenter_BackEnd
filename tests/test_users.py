import unittest
from flask import Blueprint
from unittest.mock import patch, MagicMock
from ...ClientCenter_BackEnd.models import User
from ...ClientCenter_BackEnd.modules.users_bp import login_post, client
from ...ClientCenter_BackEnd import create_app, db

class TestLogin(unittest.TestCase):

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

    @patch('ClientCenter_BackEnd.db')
    @patch('ClientCenter_BackEnd.modules.users_bp.hashlib')
    def test_login_post_success(self, mock_hashlib, mock_db):
        # Configure test data
        test_user = User(id=1, nombre='Test', apellido='User', documento_identidad='123456789')
        mock_db.session.execute.return_value.scalars.return_value.first.return_value = test_user
        mock_hashlib.sha256.return_value.hexdigest.return_value = 'hashed_password'

        # Simulate a POST request with valid data
        response = self.client.post('/login', json={'id': '1', 'password': 'password'})

        # Verify the response
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], 'Credenciales validas, bienvenido')

    @patch('ClientCenter_BackEnd.db')
    def test_login_post_invalid_credentials(self, mock_db):
        # Configure test data for a non-existent user
        mock_db.session.execute.return_value.scalars.return_value.first.return_value = None

        # Simulate a POST request with invalid login data
        response = self.client.post('/login', json={'id': '1', 'password': 'password'})

        # Verify the response
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Credenciales inválidas. Verifica e intenta de nuevo.')

class TestClient(unittest.TestCase):

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

    @patch('ClientCenter_BackEnd.db')
    def test_client_found(self, mock_db):
        # Configure test data for an existing client
        test_user = User(id=1, nombre='Test', apellido='User', documento_identidad='123456789')
        mock_db.session.execute.return_value.scalars.return_value.first.return_value = test_user

        # Simulate a GET request for an existing client
        response = self.client.get('/client/1')

        # Verify the response
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], 'Cliente encontrado')

    @patch('ClientCenter_BackEnd.db')
    def test_client_not_found(self, mock_db):
        # Configure test data for a non-existent client
        mock_db.session.execute.return_value.scalars.return_value.first.return_value = None

        # Simulate a GET request for a non-existent client
        response = self.client.get('/client/1')

        # Verify the response
        self.assertEqual(response.status_code, 404)
        data = response.json
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Usuario no encontrado.')

if __name__ == '__main__':
    unittest.main()
