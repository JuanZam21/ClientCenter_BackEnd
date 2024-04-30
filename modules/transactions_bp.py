import json
from sqlalchemy.orm.exc import NoResultFound
from .. import db
from flask import Blueprint, jsonify, request
from collections import defaultdict
from flasgger import swag_from
from ..models import User, Transactions, Transaction_type

transactions_bp = Blueprint('transactions_bp', __name__)

# Consulta de preguntas transacciones
@transactions_bp.route('/api/transaccion/questions')
@swag_from({
    'description': 'Devuelve una lista de preguntas disponibles para la consulta de transacciones',
    'tags': ['Transacciones'],
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
                                        'label': {'type': 'string', 'description': 'Etiqueta descriptiva de la pregunta'},
                                        'name': {'type': 'string', 'description': 'Nombre del campo asociado a la pregunta'}
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
      "label": "Monto",
      "name": "monto"
    },
    {
      "label": "Fecha de transaccion",
      "name": "fechaTransaccion"
    }
  ],
  "success": True,
  "message": "Preguntas encontradas"
}),200


# Consulta de transaccion por id de persona
@transactions_bp.route('/api/transaccion', methods=['POST'])
@swag_from({
    'description': 'Realiza o consulta una transacción asociada con un cliente especificado por su ID',
    'tags': ['Transacciones'],
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
                    'monto': {'type': 'boolean', 'description': 'Monto de la transacción', 'default': False},
                    'fechaTransaccion': {'type': 'boolean', 'description': 'Fecha de la transacción en formato YYYY-MM-DD', 'default': False}
                }
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Transacción procesada correctamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'message': {'type': 'string'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'descripcion': {'type': 'string'},
                            'Tipo_transaccion': {
                                'type': 'object',
                                'properties': {
                                    'name': {'type': 'string'}
                                }
                            },
                            'monto': {'type': 'number'},
                            'fechaTransaccion': {'type': 'string'}
                        }
                    }
                }
            }
        },
        '400': {
            'description': 'Información requerida faltante o incorrecta',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'message': {'type': 'string'}
                }
            }
        },
        '404': {
            'description': 'Cliente no encontrado',
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
def transaccion():
    data = request.get_json()
    
    id_cliente = data.get('idCliente')
    monto = data.get('monto')
    fecha_transaccion = data.get('fechaTransaccion')
    
    if not id_cliente:
        return jsonify({
            'success': False,
            'message': 'No se proporcionó el id del cliente'
        }), 400
    
    try:
        # Consulta la tabla user para encontrar el usuario con el id_cliente proporcionado
        user = db.session.query(User).filter(User.documento_identidad == id_cliente).first()
        # Obtiene el user_id del objeto user
        user_id = user.id
        # Consulta la tabla Transacciones para encontrar todos los datos asociados con el user_id
        transactions = db.session.query(Transactions).filter(Transactions.id_persona == user_id).all()

    except NoResultFound:
        return jsonify({
            'success': False,
            'message': 'No se encontraron creditos para el cliente proporcionado'
        }), 404
    
    transaction = transactions[0]
    transactions_dict = defaultdict()
    # Se obtiene el nombre del tipo de transaccion para mostrarlo en la respuesta
    id_transaction = transaction.id_tipo_transaccion
    transaction_type = db.session.query(Transaction_type).filter(Transaction_type.id == id_transaction).first()
    

    transaction_dict = {
        'data': {
            'descripcion': transaction.descripcion,
            'Tipo_transaccion': {
                'name':   transaction_type.name,
            },
           
        },
        'success': True,
        'message': 'Transaccion encontrada'
    }
    
    if monto:
        transaction_dict['data']['monto'] = transaction.monto
    if fecha_transaccion:
        transaction_dict['data']['fecha_transaccion'] = transaction.fecha_transaccion
    
    return jsonify(transaction_dict), 200