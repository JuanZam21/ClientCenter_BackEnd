from collections import defaultdict
from flask import jsonify
from .. import db
from sqlalchemy.orm.exc import NoResultFound
from flask import Blueprint, jsonify
from flasgger import swag_from
from ..models import History, User

graphs_bp = Blueprint('graphs_bp', __name__)

# Endpoint grafico estado de llamadas
@graphs_bp.route('/graphs/call_duration/<employee_doc>', methods=['GET'])
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

    
    employee_dict = {}

    # Itera sobre los registros de duración de llamada en la columna "duracion_llamada" y los guarda en un diccionario con la fecha como clave que está en la columna "fecha_atencion"
    for record in history:
        date_str = record.fecha_atencion.strftime('%Y-%m-%d')  
        employee_dict[date_str] = record.duracion_llamada


    return jsonify({
        'data': employee_dict,
        'success': True,
        'message': 'Duración de llamadas encontrada'
    }), 200

# Endpoint grafico estado de lamadas
@graphs_bp.route('/graphs/call_status/<employee_doc>', methods=['GET'])
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
                'message': f'Ocurrió un error: {str(e)}'
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

# Endpoint grafico conteo de llamadas
@graphs_bp.route('/graphs/call_count/<employee_doc>', methods=['GET'])
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
