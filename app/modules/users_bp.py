from flask import Blueprint, jsonify, request
from .. import db
from flasgger import swag_from
from ..models import User
import hashlib
from .save_history import save_history

users_bp = Blueprint('users_bp', __name__)

@users_bp.route('/login', methods=['POST'])
@swag_from({
    'tags': ['Empleados'],
    'description': 'Inicia sesión con un ID de usuario y una contraseña.',
    'parameters': [
        {
            'in': 'body',
            'name': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {
                        'type': 'string',
                        'description': 'El ID del usuario.'
                    },
                    'password': {
                        'type': 'string',
                        'description': 'La contraseña del usuario.'
                    }
                },
                'required': ['id', 'password']
            },
            'description': 'JSON con el ID y la contraseña del usuario.'
        }
    ],
    'responses': {
        '200': {
            'description': 'Inicio de sesión exitoso',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'message': {
                                'type': 'string',
                                'description': 'El mensaje de estado.'
                            },
                            'success': {
                                'type': 'boolean',
                                'description': 'El estado de éxito.'
                            },
                            'nombre': {
                                'type': 'string',
                                'description': 'El nombre del usuario.'
                            },
                            'apellido': {
                                'type': 'string',
                                'description': 'El apellido del usuario.'
                            },
                            'documento_identidad': {
                                'type': 'string',
                                'description': 'El documento de identidad del usuario.'
                            }
                        }
                    }
                }
            }
        },
        '400': {
            'description': 'Solicitud incorrecta',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'message': {
                                'type': 'string',
                                'description': 'El mensaje de estado.'
                            },
                            'success': {
                                'type': 'boolean',
                                'description': 'El estado de éxito.'
                            }
                        }
                    }
                }
            }
        }
    }
})
def login_post():
    data = request.get_json()
    id = data.get('id')
    password = data.get('password')
    user = db.session.execute(db.select(User).where(User.documento_identidad == id)).scalars().first()
    encoded_pass_in = password.encode('UTF-8')
    hash_pass_in = hashlib.sha256(encoded_pass_in).hexdigest()

    if not user or not (user.contrasena == hash_pass_in):
        return jsonify({'success': False, 'message': 'Credenciales inválidas. Verifica e intenta de nuevo.'}), 404

    return jsonify({
        'message': 'Credenciales validas, bienvenido',
        'success': True,
        'data': {
            'id': user.id,
            'nombre': user.nombre,
            'apellido': user.apellido,
            'documento_identidad': user.documento_identidad,
        }
    }), 200

@users_bp.route('/client/<id>')
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
    user = db.session.execute(db.select(User).where(User.documento_identidad == id)).scalars().first()

    if not user:
        return jsonify({
            'message': 'Usuario no encontrado.',
            'success': False,
        }), 404

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
