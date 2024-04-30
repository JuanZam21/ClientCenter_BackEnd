import json
from sqlalchemy.orm.exc import NoResultFound
from .. import db
from flask import Blueprint, jsonify, request
from collections import defaultdict
from flasgger import swag_from
from ..models import User, Accounts, Account_type

cards_bp = Blueprint('cards_bp', __name__)

# Consulta de preguntas tarjeats
@cards_bp.route('/api/tarjeta/questions')
def question():
    return jsonify(
        {
  "data": [
    {
      "label": "Fecha de emision",
      "name": "fechaEmision"
    },
    {
      "label": "Fecha de vencimiento",
      "name": "fechaVencimiento"
    },
    {
      "label": "Fecha de corte",
      "name": "fechaCorte"
    },
    {
      "label": "Cupo total",
      "name": "cupoTotal"
    },
    {
      "label": "Tasa de interes",
      "name": "tasaInteres"
    },
    {
      "label": "Estado",
      "name": "estado"
    },
    {
      "label": "Pago minimo",
      "name": "pagoMinimo"
    },
    {
      "label": "Pago total",
      "name": "pagoTotal"
    },
    {
      "label": "Programa de puntos",
      "name": "programaPuntos"
    }
  ],
  "success": True,
  "message": "Preguntas encontradas"
}),200

@cards_bp.route('/api/tarjeta', methods=['POST'])
def tarjeta():
    data = request.get_json()
    id_cliente = data.get('idCliente')
    fecha_emision = data.get('fechaEmision')
    fecha_vencimiento = data.get('fechaVencimiento')
    fecha_corte = data.get('fechaCorte')
    cupo_total = data.get('cupoTotal')
    tasa_interes = data.get('tasaInteres')
    estado = data.get('estado')
    pago_minimo = data.get('pagoMinimo')
    pago_total = data.get('pagoTotal')
    programa_puntos = data.get('programaPuntos')
    
    if not id_cliente:
        return jsonify({
            'success': False,
            'message': 'No se proporcionó el id del cliente'
        }), 400
    
    try:
        # Consulta la tabla User para encontrar el usuario con el id_cliente proporcionado
        user = db.session.query(User).filter(User.documento_identidad == id_cliente).first()
        # Obtiene el user_id del objeto user
        user_id = user.id
        user_name = user.nombre
        user_last_name = user.apellido
        # Consulta la tabla Accounts para encontrar todos los datos asociados con el user_id
        accounts = db.session.query(Accounts).filter(Accounts.id_persona == user_id).all()

    except NoResultFound:
        return jsonify({
            'success': False,
            'message': 'No se encontraron creditos para el cliente proporcionado'
        }), 404
    
    accounts = accounts[0]
    account_dict = defaultdict()
    id_account = accounts.id_tipo_cuenta
    account_type = db.session.query(Account_type).filter(Account_type.id == id_account).first()
    

    account_dict = {
        'data': {
            'id_cuenta': accounts.id_cuenta,
            'Persona': {
                'nombre':   user_name,
                'apellido': user_last_name
            },
            'tipo_cuenta': {
                'name': account_type.name
            }
        },
        'success': True,
        'message': 'Cuenta encontrada'
    }
    
    if saldo_actual:
        account_dict['data']['saldoActual'] = accounts.saldo_actual
    if fecha_apertura:
        account_dict['data']['fechaApertura'] = accounts.fecha_apertura
    if fecha_cierre:
        account_dict['data']['fechaCierre'] = accounts.fecha_cierre
    if beneficios:
        account_dict['data']['beneficios'] = accounts.beneficios
    if estado:
        account_dict['data']['estado'] = accounts.estado_cuenta
    
    return jsonify(account_dict), 200
