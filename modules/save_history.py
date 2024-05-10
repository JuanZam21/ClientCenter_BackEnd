from .. import db
from flask import jsonify, Blueprint
from flasgger import swag_from
from ..models import History

save_history_bp = Blueprint('save_history_bp', __name__)

def save_history(client_id, employee_id, category, status):

    # Consulta cuántos registros hay en la tabla History
    cantidad_registros = db.session.query(History).count()

    history = History(id_atencion=cantidad_registros+1 ,id_cliente=client_id, id_empleado=employee_id, categoria=category, estado=status)
    db.session.add(history)
    db.session.commit()
    return jsonify({'message': 'Historial guardado exitosamente'}), 200