import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from flask_cors import CORS
from . import config

# Initialize SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    swagger = Swagger(app)

    # Load the appropriate configuration based on environment variables
    if 'DBNAME_DEV' not in os.environ:
        app.config.from_object(config.config['production'])
        db_uri = get_database_uri(app)
    else:
        app.config.from_object(config.config['development'])
        db_uri = get_database_uri(app)

    # Set the SQLAlchemy database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    # Initialize the database with the app
    db.init_app(app)

    # Register blueprints
    from .modules.users_bp import users_bp as users_blueprint
    app.register_blueprint(users_blueprint, url_prefix='/api/auth')

    # Add other blueprints as needed
    from .modules.credits_bp import credits_bp as credits_blueprint
    app.register_blueprint(credits_blueprint)

    from .modules.accounts_bp import accounts_bp as accounts_blueprint
    app.register_blueprint(accounts_blueprint)

    from .modules.offices_bp import offices_bp as offices_blueprint
    app.register_blueprint(offices_blueprint, url_prefix='/api')

    from .modules.cards_bp import cards_bp as cards_blueprint
    app.register_blueprint(cards_blueprint)

    from .modules.transactions_bp import transactions_bp as transactions_blueprint
    app.register_blueprint(transactions_blueprint)

    return app

def get_database_uri(app):
    database = app.config.get('DBNAME')
    user = app.config.get('DBUSER')
    password = app.config.get('DBPASS')
    host = app.config.get('DBHOST')
    port = app.config.get('DBPORT')
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
