import hashlib
from flask_login import login_user, login_required, logout_user
from flask import Blueprint, redirect, url_for, request, jsonify
from .models import User, Agent
from sqlalchemy.orm.exc import NoResultFound
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login_post():
    # Se leen los datos del formulario de inicio de sesión
    data = request.get_json()

    id = data.get('id ')
    password = data.get('password')

    # Se busca al usuario en la BD y se calcula el hash de la clave introducida
    user = db.session.execute(db.select(User).where(User.documento_identidad == id)).scalars().first()
    encoded_pass_in = password.encode('UTF-8')
    hash_pass_in = hashlib.sha256(encoded_pass_in).hexdigest()

    # Si el usuario no existe o los hash no coinciden se notifica en un mensaje
    if not user or not (user.contrasena == hash_pass_in):
        # Response in json with code status 200
        return jsonify({'success': False, 'message': 'Credenciales inválidas. Verifica e intenta de nuevo.'}), 200

    # Se permite el acceso si las credenciales son váildas
    login_user(user)

    # Devolver una respuesta JSON indicando éxito
    return jsonify({
        'message': 'Credenciales validas, bienvenido',
        'success': True,
    }), 200