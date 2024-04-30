import json
from sqlalchemy.orm.exc import NoResultFound
from .. import db
from flask import Blueprint, jsonify, request
from flasgger import swag_from
from ..models import Sucursales

offices_bp = Blueprint('offices_bp', __name__)

# Consulta de todas las sucursales
@offices_bp.route('/sucursales')
@swag_from({
    'tags': ['Sucursales'], 
    'description': 'Consulta todas las sucursales disponibles en la base de datos.',
    'responses': {
        '200': {
            'description': 'Consulta exitosa de las sucursales.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'message': {
                                'type': 'string',
                                'example': 'Consulta exitosa.'
                            },
                            'success': {
                                'type': 'boolean',
                                'example': True
                            },
                            'data': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'id_sucursal': {
                                            'type': 'integer',
                                            'example': 1
                                        },
                                        'nombre_sucursal': {
                                            'type': 'string',
                                            'example': 'Sucursal Centro'
                                        },
                                        'ciudad': {
                                            'type': 'string',
                                            'example': 'Ciudad Central'
                                        },
                                        'pais': {
                                            'type': 'string',
                                            'example': 'País'
                                        }
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
def sucursales():
     # Obtener la sucursal de la base de datos
    sucursales = db.session.execute(db.select(Sucursales)).scalars().all()

    results=[]

    for sucursal in sucursales:
        result = {
        'id_sucursal': sucursal.id_sucursal,
        'nombre_sucursal': sucursal.nombre_sucursal,
        'ciudad': sucursal.ciudad,
        'departamento': sucursal.departamento,
        'pais': sucursal.pais
        }
        results.append(result)
    
    # Si la sucursal existe, devolver sus datos
    return jsonify({
        'message': 'Consulta exitosa.',
        'success': True,
        'data': results
        },
    ), 200

# Consulta de sucursales por id sucursal
@offices_bp.route('/sucursal/<id>')
@swag_from({
    'tags': ['Sucursales'],
    'description': 'Consulta  sucursales por id.',
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'string',
            'required': 'true',
            'description': 'ID of the Sucursal'
        }
    ],
    'responses': {
        '200': {
            'description': 'Sucursal found',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'message': {
                                'type': 'string'
                            },
                            'success': {
                                'type': 'boolean'
                            },
                            'sucursal': {
                                'type': 'object',
                                'properties': {
                                    'id_sucursal': {'type': 'integer'},
                                    'nombre_sucursal': {'type': 'string'},
                                    'ciudad': {'type': 'string'},
                                    'departamento': {'type': 'string'},
                                    'pais': {'type': 'string'},
                                    'direccion': {'type': 'string'},
                                    'telefono': {'type': 'string'}
                                }
                            }
                        }
                    }
                }
            }
        },
        '404': {
            'description': 'Sucursal not found',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'message': {
                                'type': 'string'
                            },
                            'success': {
                                'type': 'boolean'
                            }
                        }
                    }
                }
            }
        }
    }
})
def sucursal(id):
    # Obtener la sucursal de la base de datos
    sucursal = db.session.execute(db.select(Sucursales).where(Sucursales.id_sucursal == id)).scalars().first()

    # Si la sucursal no existe se notifica en un mensaje
    if not sucursal: 
        return jsonify({
            'message': 'Sucursal no encontrada.',
            'success': False,
        }), 404

    # Si la sucursal existe, devolver sus datos
    return jsonify({
        'message': 'Sucursal encontrada.',
        'success': True,
        'sucursal': {
            'id_sucursal': sucursal.id_sucursal,
            'nombre_sucursal': sucursal.nombre_sucursal,
            'ciudad': sucursal.ciudad,
            'departamento': sucursal.departamento,
            'pais': sucursal.pais,
            'direccion': sucursal.direccion,
            'telefono': sucursal.telefono,
        },
    }), 200