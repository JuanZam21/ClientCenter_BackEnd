import unittest
from unittest.mock import patch, MagicMock
from ..modules.users_bp import login_post, client
from .. import app
from ..models import User

class TestLogin(unittest.TestCase):

    def setUp(self):
        # Configurar un cliente de prueba falso
        self.client = app.test_client()
        # Configurar el contexto de la aplicación
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        # Pop del contexto de la aplicación
        self.app_context.pop()

    @patch('your_module.db')
    @patch('your_module.hashlib')
    def test_login_post_success(self, mock_hashlib, mock_db):
        # Configurar datos de prueba
        test_user = User(id=1, nombre='Test', apellido='User', documento_identidad='123456789')
        mock_db.session.execute.return_value.scalars.return_value.first.return_value = test_user
        mock_hashlib.sha256.return_value.hexdigest.return_value = 'hashed_password'

        # Simular una solicitud POST con datos válidos
        response = self.client.post('/login', json={'id': '1', 'password': 'password'})

        # Verificar la respuesta
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], 'Credenciales validas, bienvenido')

    @patch('your_module.db')
    def test_login_post_invalid_credentials(self, mock_db):
        # Configurar datos de prueba para un usuario no existente
        mock_db.session.execute.return_value.scalars.return_value.first.return_value = None

        # Simular una solicitud POST con datos de inicio de sesión inválidos
        response = self.client.post('/login', json={'id': '1', 'password': 'password'})

        # Verificar la respuesta
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Credenciales inválidas. Verifica e intenta de nuevo.')

class TestClient(unittest.TestCase):

    def setUp(self):
        # Configurar un cliente de prueba falso
        self.client = app.test_client()
        # Configurar el contexto de la aplicación
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        # Pop del contexto de la aplicación
        self.app_context.pop()

    @patch('your_module.db')
    def test_client_found(self, mock_db):
        # Configurar datos de prueba para un cliente existente
        test_user = User(id=1, nombre='Test', apellido='User', documento_identidad='123456789')
        mock_db.session.execute.return_value.scalars.return_value.first.return_value = test_user

        # Simular una solicitud GET para un cliente existente
        response = self.client.get('/client/1')

        # Verificar la respuesta
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], 'Cliente encontrado')

    @patch('your_module.db')
    def test_client_not_found(self, mock_db):
        # Configurar datos de prueba para un cliente no existente
        mock_db.session.execute.return_value.scalars.return_value.first.return_value = None

        # Simular una solicitud GET para un cliente no existente
        response = self.client.get('/client/1')

        # Verificar la respuesta
        self.assertEqual(response.status_code, 404)
        data = response.json
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Usuario no encontrado.')

if __name__ == '__main__':
    unittest.main()
