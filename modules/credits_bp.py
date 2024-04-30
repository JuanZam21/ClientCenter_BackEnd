import json
from sqlalchemy.orm.exc import NoResultFound
from collections import defaultdict
from .. import db
from flask import Blueprint, jsonify, request
from flasgger import swag_from
from ..models import Credit, User

credits_bp = Blueprint('credits_bp', __name__)

# Consulta de sucursales por id sucursal
@credits_bp.route('/api/credito/questions')
@swag_from({
    'tags': ['Creditos'],
    'description': 'Consulta las preguntas necesarias relacionadas a los creditos.',   
    'responses': {
        '200': {
            'description': 'Question data',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
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

def questions():
    
    return jsonify(
{
  "data": [
    {
      "label": "Monto original",
      "name": "montoOriginal"
    },
    {
      "label": "Saldo pendiente",
      "name": "saldoPendiente"
    },
    {
      "label": "Tasa de interes",
      "name": "tasaInteres"
    },
    {
      "label": "Fecha de inicio",
      "name": "fechaInicio"
    },
    {
      "label": "Fecha de finalizacion",
      "name": "fechaFinalizacion"
    },
    {
      "label": "Estado",
      "name": "estado"
    }
  ],
  "success": True,
  "message": "Preguntas encontradas"
},
    ), 200


@credits_bp.route('/api/credito', methods=['POST'])
@swag_from({
    'description': 'Consulta los creditos de una persona por su id',
    'tags': ['Creditos'],
    'consumes': ['application/json'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'idCliente': {'type': 'string', 'description': 'ID of the client'},
                    'montoOriginal': {'type': 'boolean', 'description': 'Flag to include original amount of the credit in the response', 'default': False},
                    'saldoPendiente': {'type': 'boolean', 'description': 'Flag to include pending balance of the credit in the response', 'default': False},
                    'tasaInteres': {'type': 'boolean', 'description': 'Flag to include interest rate of the credit in the response', 'default': False},
                    'fechaInicio': {'type': 'boolean', 'description': 'Flag to include start date of the credit in the response', 'default': False},
                    'fechaFinalizacion': {'type': 'boolean', 'description': 'Flag to include end date of the credit in the response', 'default': False},
                    'estado': {'type': 'boolean', 'description': 'Flag to include state of the credit in the response', 'default': False}
                }
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Credit found',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'message': {'type': 'string'},
                            'success': {'type': 'boolean'},
                            'data': {
                                'type': 'object',
                                'properties': {
                                    'tipo_credito': {'type': 'string'},
                                    'Persona': {
                                        'type': 'object',
                                        'properties': {
                                            'nombre': {'type': 'string'},
                                            'apellido': {'type': 'string'}
                                        }
                                    },
                                    'montoOriginal': {'type': 'number', 'description': 'Original amount of the credit'},
                                    'fechaFinalizacion': {'type': 'string', 'description': 'End date of the credit'}
                                }
                            }
                        }
                    }
                }
            }
        },
        '404': {
            'description': 'Credit not found',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'message': {'type': 'string'},
                            'success': {'type': 'boolean'}
                        }
                    }
                }
            }
        },
        '400': {
            'description': 'No client ID provided',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'message': {'type': 'string'},
                            'success': {'type': 'boolean'}
                        }
                    }
                }
            }
        }
    }
})
# Consulta de creditos por id de persona
def creditos_persona():
    data = request.get_json()
    id_cliente = data.get('idCliente')
    monto_original = data.get('montoOriginal')
    saldo_pendiente = data.get('saldoPendiente')
    tasa_interes = data.get('tasaInteres')
    fecha_inicio = data.get('fechaInicio')
    fecha_finalizacion = data.get('fechaFinalizacion')
    estado = data.get('estado')
    
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
        # Consulta la tabla Credit para encontrar todos los créditos asociados con el user_id
        creditos = db.session.query(Credit).filter(Credit.id_persona == user_id).all()

    except NoResultFound:
        return jsonify({
            'success': False,
            'message': 'No se encontraron creditos para el cliente proporcionado'
        }), 404
    
    credito = creditos[0]
    credit_dict = defaultdict()
    credit_dict['tipo_credito'] = credito.tipo_credito  # Assuming `tipo_credito` is a field in `credito`
    credit_dict['Persona'] = {
        'nombre':   user_name,
        'apellido': user_last_name
    }
    if monto_original:
        credit_dict['monto_original'] = credito.monto_original
    if saldo_pendiente:
        credit_dict['saldo_pendiente'] = credito.saldo_pendiente
    if tasa_interes:
        credit_dict['tasa_interes'] = credito.tasa_interes
    if fecha_inicio:
        credit_dict['fecha_inicio'] = credito.fecha_inicio
    if fecha_finalizacion:
        credit_dict['fecha_finalizacion'] = credito.fecha_finalizacion
    if estado:
        credit_dict['estado_credito'] = credito.estado_credito
    
    return jsonify({
        'success': True,
        'message': 'Creditos encontrados',
        'data': credit_dict
    }), 200