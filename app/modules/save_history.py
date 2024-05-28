from .. import db
from flask import jsonify, Blueprint, request
from ..models import History, User
from datetime import datetime
from flasgger import swag_from

save_history_bp = Blueprint('save_history_bp', __name__)

# Toma la fecha .today y resta con el valor almacenado de la fecha atencion y lo guarda en duracion llamada
@save_history_bp.route('/call_duration', methods=['POST'])
@swag_from(
    {
        'tags': ['Historial de Llamadas'],
        'description': 'Guarda la duración de una llamada en la base de datos',
        'parameters': [
            {
                'in': 'body',
                'name': 'body',
                'required': True,
                'schema': {
                    'properties': {
                        'idEmpleado': {
                            'type': 'integer',
                            'description': 'El ID del empleado'
                        },
                        'idCliente': {
                            'type': 'integer',
                            'description': 'El ID del cliente'
                        },
                        'estado': {
                            'type': 'string',
                            'description': 'El nuevo estado de la llamada'
                        }
                    }
                }
            }
        ],
        'responses': {
            '200': {
                'description': 'Éxito: La duración de la llamada se guardó correctamente',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'message': {
                                    'type': 'string',
                                    'description': 'Mensaje indicando que la duración de la llamada se guardó correctamente'
                                }
                            }
                        }
                    }
                }
            },
            '404': {
                'description': 'No se encontró un estado activo o un registro actualizado'
            }
        }
    }
)
def call_duration():
    data = request.get_json()
    employee_id = data.get('idEmpleado')
    client_id = data.get('idCliente')
    new_status = data.get('estado') 

    status = db.session.query(History).filter(
        History.id_cliente == client_id,
        History.id_empleado == employee_id,
        History.estado == "activo"
    ).first()
 
    if not status:
        return jsonify({'message': 'No se encuentra un estado activo'}), 404

    status.estado = new_status
    db.session.commit()

    call = db.session.query(History).filter(
        History.id_cliente == client_id,
        History.id_empleado == employee_id,
        History.estado == new_status
    ).first()
    
    if not call:
        return jsonify({'message': 'No se encuentra un registro actualizado'}), 404
    
    # Calcular duracion de llamada en segundos
    call_duration = (datetime.today() - call.fecha_atencion).total_seconds()

    call.duracion_llamada = call_duration
    db.session.commit()
    
    return jsonify({'message': 'Duración de llamada guardada exitosamente'}), 200


# Función para poblar la tabla historial_atencion_cliente
def save_history(client_id, employee_id, category, date, type, description):

    # Consulta cuántos registros hay en la tabla History
    cantidad_registros = db.session.query(History).count()

    history = History(id_atencion=cantidad_registros+1, id_cliente=client_id, id_empleado=employee_id, categoria=category, fecha_atencion=date, tipo_atencion=type, descripcion=description, estado='activo')
    db.session.add(history)
    db.session.commit()