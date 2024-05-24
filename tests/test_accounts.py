import unittest
from flask import Flask
from app import create_app

class TestAccountsAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()

    def test_questions_success(self):
        response = self.client.get('/api/cuenta/questions')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], 'Preguntas encontradas')
        self.assertIsInstance(data['data'], list)
        self.assertGreater(len(data['data']), 0)
        expected_questions = [
            {"label": "Saldo actual", "name": "saldoActual"},
            {"label": "Fecha de apertura", "name": "fechaApertura"},
            {"label": "Fecha de cierre", "name": "fechaCierre"},
            {"label": "Beneficios", "name": "beneficios"},
            {"label": "Estado", "name": "estado"}
        ]
        self.assertEqual(data['data'], expected_questions)

if __name__ == '__main__':
    unittest.main()
