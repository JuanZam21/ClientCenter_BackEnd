import json
from sqlalchemy.orm.exc import NoResultFound
from flask import Blueprint, jsonify, request
from .. import db
from flasgger import swag_from
from ..models import User

clients_bp = Blueprint('clients_bp', __name__)

# Consulta ID
@clients_bp.route('/client/<id>')
@swag_from({
    'tags': ['Clientes'],  
    'description': 'Devuelve un cliente por su ID.',
    'parameters': [
        {
            'in': 'path',
            'name': 'id',
            'schema': {
                'type': 'string'
            },
            'required': True,
            'description': 'The client ID'
        }
    ],
    'responses': {
        '200': {
            'description': 'The client was found',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'message': {
                                'type': 'string',
                                'description': 'The status message'
                            },
                            'success': {
                                'type': 'boolean',
                                'description': 'The success status'
                            },
                            'data': {
                                'type': 'object',
                                'properties': {
                                    'id': {
                                        'type': 'integer'
                                    },
                                    'nombre': {
                                        'type': 'string'
                                    },
                                    'apellido': {
                                        'type': 'string'
                                    },
                                    'documento_identidad': {
                                        'type': 'string'
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        '404': {
            'description': 'The client was not found',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'message': {
                                'type': 'string',
                                'description': 'The status message'
                            },
                            'success': {
                                'type': 'boolean',
                                'description': 'The success status'
                            }
                        }
                    }
                }
            }
        }
    }
})
def client(id):
    # Se busca al usuario en la BD y se calcula el hash de la clave introducida
    user = db.session.execute(db.select(User).where(User.documento_identidad == id)).scalars().first()

    # Si el usuario no existe se notifica en un mensaje
    if not user: 
            return jsonify({
                    'message': 'Usuario no encontrado.',
                    'success': False,
            }), 404

    # Devolver una respuesta JSON indicando éxito
    return jsonify({
    'message': 'Cliente encontrado',
    'success': True,
    'data': {
        'id': user.id,
        'nombre': user.nombre,
        'apellido': user.apellido,
        'documento_identidad': user.documento_identidad,
    }
}), 200


