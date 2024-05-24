import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, jsonify
from app import create_app, db
from app.models import User, Cards, Card_type

class TestCardsAPI(unittest.TestCase):

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

    def test_question_success(self):
        response = self.client.get('/api/tarjeta/questions')

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], 'Preguntas encontradas')
        self.assertIsInstance(data['data'], list)
        self.assertGreater(len(data['data']), 0)

    @patch('app.db')
    def test_tarjeta_success(self, mock_db):
        test_user = User(id=1, nombre='Test', apellido='User', documento_identidad='123456789')
        test_card = Cards(
            id_persona=1, id_tipo_tarjeta=1, numero_tarjeta='1234567890123456',
            ultimos_digitos='3456', nombre_titular='Test User', fecha_emision='2020-01-01',
            fecha_vencimiento='2025-01-01', fecha_corte='2024-01-01', cupo_total=10000,
            cupo_disponible=8000, saldo_actual=2000, tasa_interes=0.15, estado_tarjeta='Activa',
            cvv='123', pago_minimo=500, pago_total=1500, pago_anticipado=0, programa_puntos='Si'
        )
        test_card_type = Card_type(id=1, name='Gold')

        mock_db.session.query.return_value.filter.return_value.first.side_effect = [test_user, test_card, test_card_type]

        response = self.client.post('/api/tarjeta', json={
            'idCliente': '123456789',
            'fechaEmision': True,
            'fechaVencimiento': True,
            'fechaCorte': True,
            'cupoTotal': True,
            'tasaInteres': True,
            'estado': True,
            'pagoMinimo': True,
            'pagoTotal': True,
            'programaPuntos': True
        })

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], 'Tarjeta encontrada')
        self.assertEqual(data['data']['nombre_titular'], 'Juan García')
        self.assertEqual(data['data']['Tipo_tarjeta']['name'], 'crédito')
        self.assertEqual(data['data']['fecha_emision'], 'Sun, 01 Jan 2023 00:00:00 GMT')
        self.assertEqual(data['data']['fecha_vencimiento'], 'Wed, 01 Jan 2025 00:00:00 GMT')
        self.assertEqual(data['data']['fecha_corte'], 'Sun, 15 Jan 2023 00:00:00 GMT')
        self.assertEqual(float(data['data']['cupo_total']), 10000)  # Convert to float before asserting
        self.assertEqual(float(data['data']['tasa_interes']), 15)  # Convert to float before asserting
        self.assertEqual(data['data']['estado_tarjeta'], 'Activa')
        self.assertEqual(float(data['data']['pago_minimo']), 100)  # Convert to float before asserting
        self.assertEqual(float(data['data']['pago_total']), 200)  # Convert to float before asserting
        self.assertEqual(data['data']['programa_puntos'], 'Programa de recompensas A')

    @patch('app.db')
    def test_tarjeta_no_id_cliente(self, mock_db):
        response = self.client.post('/api/tarjeta', json={})

        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'No se proporcionó el id del cliente')

if __name__ == '__main__':
    unittest.main()