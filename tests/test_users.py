import unittest, hashlib
from unittest.mock import patch, MagicMock
from app.models import User
from app import create_app, db


class TestLogin(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

    @classmethod
    def tearDownClass(cls):
        cls.app_context.pop()

     # Test a successful login
    @patch('app.db')
    def test_login_post_successful(self, mock_db):
        hashed_password = hashlib.sha256('clave'.encode('UTF-8')).hexdigest()
        test_user = User(id=3, nombre='Pedro', apellido='López', documento_identidad='345678901', contrasena=hashed_password)
        mock_db.session.execute.return_value.scalars.return_value.first.return_value = test_user

        response = self.client.post('/api/auth/login', json={'id': '345678901', 'password': 'clave'})

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], 'Credenciales validas, bienvenido')
        self.assertEqual(data['data']['id'], test_user.id)
        self.assertEqual(data['data']['nombre'], test_user.nombre)
        self.assertEqual(data['data']['apellido'], test_user.apellido)
        self.assertEqual(data['data']['documento_identidad'], test_user.documento_identidad)

    # Test a unsuccessful login
    @patch('app.db')
    def test_login_post_invalid_password(self, mock_db):
        hashed_password = hashlib.sha256('clave'.encode('UTF-8')).hexdigest()
        test_user = User(id=3, nombre='Pedro', apellido='López', documento_identidad='345678901', contrasena=hashed_password)
        mock_db.session.execute.return_value.scalars.return_value.first.return_value = test_user
        
        response = self.client.post('/api/auth/login', json={'id': '123456789', 'password': 'clave'})
        
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Credenciales inválidas. Verifica e intenta de nuevo.')


class TestClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

    @classmethod
    def tearDownClass(cls):
        cls.app_context.pop()

    @patch('app.db')
    def test_client_found(self, mock_db):
        test_user = User(id=1, nombre='Test', apellido='User', documento_identidad='123456789')
        mock_db.session.execute.return_value.scalars.return_value.first.return_value = test_user

        response = self.client.get('/api/auth/client/123456789')

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], 'Cliente encontrado')

    @patch('app.db')
    def test_client_not_found(self, mock_db):
        mock_db.session.execute.return_value.scalars.return_value.first.return_value = None

        response = self.client.get('/api/auth/client/945456798')

        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Usuario no encontrado.')

if __name__ == '__main__':
    unittest.main()