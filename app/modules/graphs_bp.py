from collections import defaultdict
from flask import jsonify
from .. import db
from sqlalchemy.orm.exc import NoResultFound
from flask import Blueprint, jsonify
from flasgger import swag_from
from ..models import History, User

graphs_bp = Blueprint('graphs_bp', __name__)

# Datos grafico duracion de llamadas admin
@graphs_bp.route('/graphs/call_duration')
@swag_from(
    {
        'tags': ['Historial de Llamadas'],
        'description': 'Obtiene el promedio de duración de llamadas por día para el administrador',
        'responses': {
            '200': {
                'description': 'Éxito: El promedio de duración de llamadas por día se obtuvo correctamente',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'data': {
                                    'type': 'object',
                                    'description': 'Diccionario que contiene el promedio de duración redondeado de llamadas por día',
                                    'example': {
                                        '2024-05-26': 120,
                                        '2024-05-27': 105,
                                        '2024-05-28': 90
                                    }
                                }
                            }
                        }
                    }
                }
            },
            '404': {
                'description': 'No se encontraron fechas con registros de llamadas'
            },
            '500': {
                'description': 'Error del servidor al procesar la solicitud'
            }
        }
    }
)
def call_duration_admin():
    try:
        # Consulta para obtener todas las fechas en las que hubo llamadas y el promedio de duración de las llamadas para cada fecha
        call_dates = db.session.query(
            db.func.date(History.fecha_atencion).label('fecha'),
            db.func.round(db.func.avg(History.duracion_llamada), 0).label('duracion_promedio_redondeada')
        ).group_by(db.func.date(History.fecha_atencion)).all()

        if not call_dates:
            return jsonify({
                'success': False,
                'message': 'No se encontraron fechas con registros de llamadas'
            }), 404

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Ocurrió un error: {str(e)}'
        }), 500

    date_dict = {}

    # Itera sobre los resultados de la consulta y guarda las fechas y promedios redondeados de duración en un diccionario
    for record in call_dates:
        date_str = record.fecha.strftime('%Y-%m-%d')
        date_dict[date_str] = record.duracion_promedio_redondeada

    return jsonify({
        'data': date_dict,
        'success': True,
        'message': 'Promedio de duración redondeado de llamadas por día encontrado'
    }), 200

# Datos grafico duracion de llamadas por empleado
@graphs_bp.route('/graphs/call_duration/<employee_doc>')
@swag_from(
    {
        'tags': ['Historial de Llamadas'],
        'description': 'Obtiene el promedio de duración de llamadas por día para un empleado específico',
        'parameters': [
            {
                'in': 'path',
                'name': 'employee_doc',
                'type': 'string',
                'required': True,
                'description': 'El documento de identidad del empleado'
            }
        ],
        'responses': {
            '200': {
                'description': 'Éxito: El promedio de duración de llamadas por día se obtuvo correctamente',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'data': {
                                    'type': 'object',
                                    'description': 'Diccionario que contiene el promedio de duración redondeado de llamadas por día',
                                    'example': {
                                        '2024-05-26': 120,
                                        '2024-05-27': 105,
                                        '2024-05-28': 90
                                    }
                                }
                            }
                        }
                    }
                }
            },
            '404': {
                'description': 'No se encontraron registros de llamadas para el empleado proporcionado'
            },
            '500': {
                'description': 'Error del servidor al procesar la solicitud'
            }
        }
    }
)
def call_duration(employee_doc):
    
    if not employee_doc:
        return jsonify({
            'success': False,
            'message': 'No se proporcionó el id del empleado'
        }), 400 
    
    try:
        # Consulta la tabla History para encontrar el empleado con el employee_id proporcionado
        employee = db.session.query(User).filter(User.documento_identidad == employee_doc).first()

        if not employee:
            return jsonify({
                'success': False,
                'message': 'Empleado no encontrado'
            }), 404

        employee_id = employee.id

        # Consulta los registros tabla History asociados al empleado
        history = db.session.query(
            db.func.date(History.fecha_atencion).label('fecha'),
            db.func.round(db.func.avg(History.duracion_llamada), 0).label('duracion_promedio_redondeada')
        ).filter(History.id_empleado == employee_id).group_by(db.func.date(History.fecha_atencion)).all()

        if not history:
            return jsonify({
                'success': False,
                'message': 'No se encontraron registros de llamadas para el empleado proporcionado'
            }), 404

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Ocurrió un error: {str(e)}'
        }), 500

    employee_dict = {}

    # Itera sobre los resultados de la consulta y guarda los promedios redondeados de duración en un diccionario con la fecha como clave
    for record in history:
        date_str = record.fecha.strftime('%Y-%m-%d')
        employee_dict[date_str] = record.duracion_promedio_redondeada

    return jsonify({
        'data': employee_dict,
        'success': True,
        'message': 'Duración promedio redondeada de llamadas por día encontrada'
    }), 200

# Datos grafico estado de llamadas admin
@graphs_bp.route('/graphs/call_status')
@swag_from(
    {
        'tags': ['Historial de Llamadas'],
        'description': 'Obtiene el estado de las llamadas para el administrador',
        'responses': {
            '200': {
                'description': 'Éxito: El estado de las llamadas se obtuvo correctamente',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'data': {
                                    'type': 'object',
                                    'description': 'Diccionario que contiene el conteo de llamadas en estado "resuelto" y "activo"',
                                    'properties': {
                                        'resuelto': {
                                            'type': 'integer',
                                            'description': 'Número de llamadas en estado "resuelto"'
                                        },
                                        'activo': {
                                            'type': 'integer',
                                            'description': 'Número de llamadas en estado "activo"'
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            '500': {
                'description': 'Error del servidor al procesar la solicitud'
            }
        }
    }
)
def call_status_admin():
    try:
        # Consulta agregada para contar los registros de estado "resuelto" y "activo"
        status_counts = db.session.query(
            History.estado,
            db.func.count(History.estado).label('count')
        ).group_by(History.estado).all()

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Ocurrió un error en admin: {str(e)}'
        }), 500

    # Diccionario para almacenar los conteos
    status_dict = {
        "resuelto": 0,
        "activo": 0
    }

    # Itera sobre los resultados y actualiza el diccionario
    for status, count in status_counts:
        if status == "resuelto":
            status_dict["resuelto"] = count
        elif status == "activo":
            status_dict["activo"] = count

    return jsonify({
        'data': status_dict,
        'success': True,
        'message': 'Estado de llamadas encontrado'
    }), 200

# Datos grafico estado de llamadas por empleado
@graphs_bp.route('/graphs/call_status/<employee_doc>')
@swag_from(
    {
        'tags': ['Historial de Llamadas'],
        'description': 'Obtiene el estado de las llamadas para un empleado específico',
        'parameters': [
            {
                'in': 'path',
                'name': 'employee_doc',
                'type': 'string',
                'required': True,
                'description': 'El documento de identidad del empleado'
            }
        ],
        'responses': {
            '200': {
                'description': 'Éxito: El estado de las llamadas para el empleado se obtuvo correctamente',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'data': {
                                    'type': 'object',
                                    'description': 'Diccionario que contiene el conteo de llamadas en estado "resuelto" y "activo"',
                                    'properties': {
                                        'resuelto': {
                                            'type': 'integer',
                                            'description': 'Número de llamadas en estado "resuelto"'
                                        },
                                        'activo': {
                                            'type': 'integer',
                                            'description': 'Número de llamadas en estado "activo"'
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            '404': {
                'description': 'No se encontraron registros de llamadas para el empleado proporcionado'
            },
            '500': {
                'description': 'Error del servidor al procesar la solicitud'
            }
        }
    }
)
def call_status(employee_doc):
    
    if not employee_doc:
        return jsonify({
            'success': False,
            'message': 'No se proporcionó el id del empleado'
        }), 400 
    
    try:
        # Consulta la tabla History para encontrar el empleado con el employee_id proporcionado
        employee = db.session.query(User).filter(User.documento_identidad == employee_doc).first()

        if not employee:
                    return jsonify({
                        'success': False,
                        'message': 'Empleado no encontrado'
                    }), 404

        employee_id = employee.id

        # Consulta los registros tabla History asociados al empleado
        history = db.session.query(History).filter(History.id_empleado == employee_id).all()

        if not history:
            return jsonify({
                'success': False,
                'message': 'No se encontraron registros de llamadas para el empleado proporcionado'
            }), 404

    except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Ocurrió un error en employee: {str(e)}'
            }), 500

    employee_dict = {
        "resuelto": 0,
        "activo": 0
    }

    # Itera sobre los registros de estado de llamada para el empleado
    for record in history:
        # Contar cuantos llamadas tiene en estado "resuelto" y cuantas en "activo" en la columna estado para ese empleado
        if record.estado == "resuelto":
            employee_dict["resuelto"] += 1
        else:
            employee_dict["activo"] += 1

    return jsonify({
        'data': employee_dict,
        'success': True,
        'message': 'Duración de llamadas encontrada'
    }), 200

# Datos grafico conteo de llamadas admin
@graphs_bp.route('/graphs/call_count')
@swag_from(
    {
        'tags': ['Historial de Llamadas'],
        'description': 'Obtiene el conteo de llamadas por fecha para el administrador',
        'responses': {
            '200': {
                'description': 'Éxito: El conteo de llamadas por fecha se obtuvo correctamente',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'data': {
                                    'type': 'object',
                                    'description': 'Diccionario que contiene el número de llamadas por fecha',
                                    'additionalProperties': {
                                        'type': 'integer'
                                    }
                                }
                            }
                        }
                    }
                }
            },
            '500': {
                'description': 'Error del servidor al procesar la solicitud'
            }
        }
    }
)
def call_count_admin():
    try:
        # Consulta agregada para contar los registros agrupados por fecha de atención
        call_counts = db.session.query(
            db.func.date(History.fecha_atencion).label('fecha'),
            db.func.count(History.id_atencion).label('count')
        ).group_by(db.func.date(History.fecha_atencion)).all()

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Ocurrió un error admin: {str(e)}'
        }), 500

    call_count_by_date = {}

    # Itera sobre los resultados y actualiza el diccionario
    for record in call_counts:
        date_str = record.fecha.strftime('%Y-%m-%d')
        call_count_by_date[date_str] = record.count

    return jsonify({
        'data': call_count_by_date,
        'success': True,
        'message': 'Número de llamadas por fecha encontrado'
    }), 200

# Datos grafico conteo de llamadas por empleado
@graphs_bp.route('/graphs/call_count/<employee_doc>')
@swag_from(
    {
        'tags': ['Historial de Llamadas'],
        'description': 'Obtiene el conteo de llamadas por fecha para un empleado específico',
        'parameters': [
            {
                'in': 'path',
                'name': 'employee_doc',
                'type': 'string',
                'required': True,
                'description': 'El documento de identidad del empleado'
            }
        ],
        'responses': {
            '200': {
                'description': 'Éxito: El conteo de llamadas por fecha para el empleado se obtuvo correctamente',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'data': {
                                    'type': 'object',
                                    'description': 'Diccionario que contiene el número de llamadas por fecha',
                                    'additionalProperties': {
                                        'type': 'integer'
                                    }
                                }
                            }
                        }
                    }
                }
            },
            '400': {
                'description': 'Error: No se proporcionó el id del empleado'
            },
            '404': {
                'description': 'Error: No se encontró el empleado con el id proporcionado'
            },
            '500': {
                'description': 'Error del servidor: Ocurrió un error al procesar la solicitud'
            }
        }
    }
)
def call_count(employee_doc):
    
    if not employee_doc:
        return jsonify({
            'success': False,
            'message': 'No se proporcionó el id del empleado'
        }), 400
    
    try:
        # Consulta la tabla User para encontrar el empleado con el employee_doc proporcionado
        employee = db.session.query(User).filter(User.documento_identidad == employee_doc).first()

        if not employee:
            return jsonify({
                'success': False,
                'message': 'Empleado no encontrado'
            }), 404

        employee_id = employee.id

        # Consulta los registros tabla History asociados al empleado
        history = db.session.query(History).filter(History.id_empleado == employee_id).all()

        if not history:
            return jsonify({
                'success': False,
                'message': 'No se encontraron registros de llamadas para el empleado proporcionado'
            }), 404

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Ocurrió un error: {str(e)}'
        }), 500

    call_count_by_date = {}

    # Itera sobre los registros de llamadas y cuenta el número de llamadas por fecha
    for record in history:
        date_str = record.fecha_atencion.strftime('%Y-%m-%d')
        if date_str not in call_count_by_date:
            call_count_by_date[date_str] = 0
        call_count_by_date[date_str] += 1

    return jsonify({
        'data': call_count_by_date,
        'success': True,
        'message': 'Número de llamadas por fecha encontrado'
    }), 200
