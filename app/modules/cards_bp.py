from sqlalchemy.orm.exc import NoResultFound
from .. import db
from flask import Blueprint, jsonify, request
from collections import defaultdict
from flasgger import swag_from
from ..models import User, Cards, Card_type
from .save_history import save_history

cards_bp = Blueprint('cards_bp', __name__)

# Consulta de preguntas tarjeats
@cards_bp.route('/api/tarjeta/questions')
@swag_from({
    'description': 'Devuelve preguntas estándar para obtener información detallada de las tarjetas de crédito',
    'tags': ['Tarjetas'],
    'responses': {
        '200': {
            'description': 'Preguntas encontradas exitosamente',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'success': {'type': 'boolean'},
                            'message': {'type': 'string'},
                            'data': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'label': {'type': 'string'},
                                        'name': {'type': 'string'}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
})
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

# Consulta de tarjeta por id de persona 
@cards_bp.route('/api/tarjeta', methods=['POST'])
@swag_from({
    'description': 'Crea o actualiza la información de la tarjeta de crédito de un cliente basado en su ID',
    'tags': ['Tarjetas'],
    'consumes': ['application/json'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'idCliente': {'type': 'string', 'description': 'ID del cliente'},
                    'fechaEmision': {'type': 'boolean', 'description': 'Fecha de emisión de la tarjeta', 'default': False},
                    'fechaVencimiento': {'type': 'boolean', 'description': 'Fecha de vencimiento de la tarjeta', 'default': False},
                    'fechaCorte': {'type': 'boolean', 'description': 'Fecha de corte de la tarjeta', 'default': False},
                    'cupoTotal': {'type': 'boolean', 'description': 'Cupo total de la tarjeta', 'default': False},
                    'tasaInteres': {'type': 'boolean', 'description': 'Tasa de interés de la tarjeta', 'default': False},
                    'estado': {'type': 'boolean', 'description': 'Estado actual de la tarjeta', 'default': False},
                    'pagoMinimo': {'type': 'boolean', 'description': 'Pago mínimo requerido', 'default': False},
                    'pagoTotal': {'type': 'boolean', 'description': 'Pago total realizado', 'default': False},
                    'programaPuntos': {'type': 'boolean', 'description': 'Programa de puntos asociado a la tarjeta', 'default': False}
                }
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Información de la tarjeta procesada correctamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'message': {'type': 'string'},
                    'data': {'$ref': '#/definitions/TarjetaInfo'}
                }
            }
        },
        '400': {
            'description': 'Datos de entrada inválidos o faltantes',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'message': {'type': 'string'}
                }
            }
        },
        '404': {
            'description': 'No se encontró al cliente con el ID proporcionado',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'message': {'type': 'string'}
                }
            }
        }
    }
})
def tarjeta():
    data = request.get_json()
    doc_cliente = data.get('idCliente')
    fecha_emision = data.get('fechaEmision')
    fecha_vencimiento = data.get('fechaVencimiento')
    fecha_corte = data.get('fechaCorte')
    cupo_total = data.get('cupoTotal')
    tasa_interes = data.get('tasaInteres')
    estado_tarjeta = data.get('estado')
    pago_minimo = data.get('pagoMinimo')
    pago_total = data.get('pagoTotal')
    programa_puntos = data.get('programaPuntos')

    # Json history
    employee_doc = data.get('idEmpleado')
    category = data.get('categoria')
    date = data.get('fechAtencion')
    type = data.get('tipoAtencion')
    description = data.get('descripcion')

    
    if not doc_cliente:
        return jsonify({
            'success': False,
            'message': 'No se proporcionó el docuemnto del cliente'
        }), 400
    
    try:
        # Consulta la tabla User para encontrar el usuario con el id_cliente proporcionado
        client = db.session.query(User).filter(User.documento_identidad == doc_cliente).first()

        # Obtiene el user_id del objeto user
        client_id = client.id


        client_name = client.nombre
        client_last_name = client.apellido
        # Consulta la tabla Accounts para encontrar todos los datos asociados con el client_id
        cards = db.session.query(Cards).filter(Cards.id_persona == client_id).all()

    except NoResultFound:
        return jsonify({
            'success': False,
            'message': 'No se encontraron tarjetas para el cliente proporcionado'
        }), 404
    
    cards = cards[0]
    cards_dict = defaultdict()
    id_account = Cards.id_tipo_tarjeta
    card_type = db.session.query(Card_type).filter(Card_type.id == id_account).first()
    
    cards_dict = {
        'data': {
            "nombre_titular": f"{client_name} {client_last_name}",
            'Tipo_tarjeta': {
                'name':   card_type.name,
             },
            
        },
        'success': True,
        'message': 'Tarjeta encontrada'
    }
    
    if fecha_emision:
        cards_dict['data']['fecha_emision'] = cards.fecha_emision
    if fecha_vencimiento:
        cards_dict['data']['fecha_vencimiento'] = cards.fecha_vencimiento
    if fecha_corte:
        cards_dict['data']['fecha_corte'] = cards.fecha_corte
    if cupo_total:
        cards_dict['data']['cupo_total'] = cards.cupo_total
    if tasa_interes:
        cards_dict['data']['tasa_interes'] = cards.tasa_interes
    if estado_tarjeta:
        cards_dict['data']['estado_tarjeta'] = cards.estado_tarjeta
    if pago_minimo:
        cards_dict['data']['pago_minimo'] = cards.pago_minimo
    if pago_total:
        cards_dict['data']['pago_total'] = cards.pago_total
    if programa_puntos:
        cards_dict['data']['programa_puntos'] = cards.programa_puntos

    # Guardar en la tabla history
    employee = db.session.query(User).filter(User.documento_identidad == employee_doc).first()
    employee_id = employee.id

    save_history(client_id, employee_id, category, date, type, description)
    
    return jsonify(cards_dict), 200