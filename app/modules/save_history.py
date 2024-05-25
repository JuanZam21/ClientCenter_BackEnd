from .. import db
from flask import jsonify, Blueprint
from ..models import History
from datetime import datetime
from flasgger import swag_from

save_history_bp = Blueprint('save_history_bp', __name__)

#Endpoint el cual toma la fecha .today y resta con el valor almacenado de la fecha_atencion en la tabla historial_atencion_cliente en su ultimo registro y lo guarda en el campo duración llamada en segundos
@save_history_bp.route('/call_duration', methods=['PUT'])
@swag_from({
    'responses': {
        200: {
            'description': 'Duración de llamada guardada exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'example': 'Duración de llamada guardada exitosamente'
                    }
                }
            }
        },
        404: {
            'description': 'No se encontró el registro',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'example': 'No se encontró el registro'
                    }
                }
            }
        }
    },
    'tags': ['Call Duration'],
    'description': 'Consulta el último registro de la tabla historial_atencion_cliente, calcula la duración de la llamada y actualiza el campo duración.'
})
def call_duration():
    # Consulta el ultimo registro de la tabla historial_atencion_cliente
    last_record = db.session.query(History).order_by(History.id_atencion.desc()).first()
    # Calcula la duración de la llamada en segundos
    call_duration = (datetime.today() - last_record.fecha_atencion).total_seconds()
    # Actualiza el campo duración en la tabla historial_atencion_cliente
    last_record.duracion_llamada = call_duration
    db.session.commit()
    return jsonify({'message': 'Duración de llamada guardada exitosamente'}), 200


# Función para poblar la tabla historial_atencion_cliente
def save_history(client_id, employee_id, category, status):

    # Consulta cuántos registros hay en la tabla History
    cantidad_registros = db.session.query(History).count()

    history = History(id_atencion=cantidad_registros+1 ,id_cliente=client_id, id_empleado=employee_id, categoria=category, estado=status)
    db.session.add(history)
    db.session.commit()
    return jsonify({'message': 'Historial guardado exitosamente'}), 200