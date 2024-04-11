import os
from . import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Inicializa SQLAlchemy para todo el proyecto
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Se determina el ambiente (Dev/Prod) y se cargan las variables de entorno
    if 'DBNAME_DEV' not in os.environ:
        app.config.from_object(config.config['production'])

        # Se asignan las variables para las cadenas de conexión a la BD en Azure
        database = app.config.get('IA_DB_NAME')
        user = app.config.get('IA_DB_USER')
        password = app.config.get('IA_DB_PASS')
        host = app.config.get('IA_DB_HOST')
        port = app.config.get('IA_DB_PORT')
        
        db_uri = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
        
    else:
        app.config.from_object(config.config['development'])

        # Se asignan las variables para la cadena de conexión a la BD local
        database = app.config.get('DBNAME')
        user = app.config.get('DBUSER')
        password = app.config.get('DBPASS')
        host = app.config.get('DBHOST')
        port = app.config.get('DBPORT')
        
        db_uri = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"

    # Se crea la cadena de conexión a la BD y la clave de la aplicación
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    # Se inicializa la aplicación
    db.init_app(app)

 