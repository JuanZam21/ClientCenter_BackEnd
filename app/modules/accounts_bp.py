from sqlalchemy.orm.exc import NoResultFound
from .. import db
from flask import Blueprint, jsonify, request
from collections import defaultdict
from flasgger import swag_from
from .save_history import save_history
from ..models import User, Accounts, Account_type

accounts_bp = Blueprint('accounts_bp', __name__)

# Consulta de preguntas cuentas
@accounts_bp.route('/api/cuenta/questions')
@swag_from({
    'description': 'Devuelve preguntas estándar para obtener información detallada de las cuentas',
    'tags': ['Cuentas'],
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
def questions():
    return jsonify(
     {
  "data": [
    {
      "label": "Saldo actual",
      "name": "saldoActual"
    },
    {
      "label": "Fecha de apertura",
      "name": "fechaApertura"
    },
    {
      "label": "Fecha de cierre",
      "name": "fechaCierre"
    },
    {
      "label": "Beneficios",
      "name": "beneficios"
    },
    {
      "label": "Estado",
      "name": "estado"
    }
  ],
  "success": True,
  "message": "Preguntas encontradas"
},

    ),200

# Consulta de cuentas por id de persona
@accounts_bp.route('/api/cuenta', methods=['POST'])
@swag_from({
    'description': 'Consulta los creditos de una persona por su id',
    'tags': ['Cuentas'],
    'consumes': ['application/json'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'idCliente': {'type': 'string'},
                    'saldoActual': {'type': 'boolean', 'default': False},
                    'fechaApertura': {'type': 'boolean', 'default': False},
                    'fechaCierre': {'type': 'boolean', 'default': False},
                    'beneficios': {'type': 'boolean', 'default': False},
                    'estado': {'type': 'boolean', 'default': False}
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
def cuenta():
    data = request.get_json()
    doc_cliente = data.get('idCliente')
    saldo_actual = data.get('saldoActual')
    fecha_apertura = data.get('fechaApertura')
    fecha_cierre = data.get('fechaCierre')
    beneficios = data.get('beneficios')
    estado = data.get('estado')

    # Json history
    employee_doc = data.get('idEmpleado')
    category = data.get('categoria')
    date = data.get('fechAtencion')
    type = data.get('tipoAtencion')
    description = data.get('descripcion')
    
    if not doc_cliente:
        return jsonify({
            'success': False,
            'message': 'No se proporcionó el id del cliente'
        }), 400
    
    try:
        # Consulta la tabla User para encontrar el usuario con el id_cliente proporcionado
        client = db.session.query(User).filter(User.documento_identidad == doc_cliente).first()
        # Obtiene el user_id del objeto user
        client_id = client.id
        client_name = client.nombre
        client_last_name = client.apellido
        # Consulta la tabla Accounts para encontrar todos los datos asociados con el client_id
        accounts = db.session.query(Accounts).filter(Accounts.id_persona == client_id).all()

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
                'nombre':   client_name,
                'apellido': client_last_name
            },
            'tipo_cuenta': {
                'name': account_type.name
            }
        },
        'success': True,
        'message': 'Cuenta encontrada'
    }
    
    if saldo_actual:
        account_dict['data']['saldo_actual'] = accounts.saldo_actual
    if fecha_apertura:
        account_dict['data']['fecha_apertura'] = accounts.fecha_apertura
    if fecha_cierre:
        account_dict['data']['fecha_cierre'] = accounts.fecha_cierre
    if beneficios:
        account_dict['data']['beneficios'] = accounts.beneficios
    if estado:
        account_dict['data']['estado_cuenta'] = accounts.estado_cuenta

    # Guardar en la tabla history
    employee = db.session.query(User).filter(User.documento_identidad == doc_cliente).first()
    employee_id = employee.id   
    
    save_history(client_id, employee_id, category, date, type, description)
 
    return jsonify(account_dict), 200