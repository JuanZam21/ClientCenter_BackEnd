import os
from dotenv import load_dotenv

# Se carga el archivo .env (en caso de existir en el ambiente de desarrollo)
load_dotenv()

# Se especifíca el tipo de ambiente (Dev/Prod)
class Config(object):
    DEBUG = True
    TESTING = False 

# Para el ambiente de desarrollo
# Se cargan las variables de entorno alojadas de forma local en archivo .env
# El acceso al Data Warehouse de Impresistem se debe hacer únicamente desde el ambiente de producción
class DevelopmentConfig(Config):

    DBNAME = os.getenv('DBNAME_DEV')
    DBHOST = os.getenv('DBHOST_DEV')
    DBPORT = os.getenv('DBPORT_DEV')
    DBUSER = os.getenv('DBUSER_DEV')
    DBPASS = os.getenv('DBPASS_DEV')

    SECRET_KEY = os.getenv('SECRET_KEY')


# Para el ambiente de producción
# Se cargan las variables de entorno configuradas en Azure Web Services
# OPENAI_KEY, SECRET_KEY y las credenciales de acceso a las BD de agentes y bodega de datos
class ProductionConfig(Config):
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_API_VERSION = os.getenv('OPENAI_API_VERSION')

    IA_DB_NAME = os.getenv('IA_NAME_DB')
    IA_DB_HOST = os.getenv('IA_PASSWORD_DB')
    IA_DB_PORT = os.getenv('IA_PORT_DB')
    IA_DB_USER = os.getenv('IA_SERVER_DB')
    IA_DB_PASS = os.getenv('IA_USER_DB')

    BI_DW_NAME = os.getenv('BI_NAME_DB')
    BI_DW_HOST = os.getenv('BI_PASSWORD_DB')
    BI_DW_PORT = os.getenv('BI_PORT_DB')
    BI_DW_USER = os.getenv('BI_SERVER_DB')
    BI_DW_PASS = os.getenv('BI_USER_DB')

    SECRET_KEY = os.getenv('SECRET_KEY')

# Se establece la configruación de la aplicación con base en el tipo de ambiente (Dev/Prod)
config = {
    'development': DevelopmentConfig,
    'testing': DevelopmentConfig,
    'production': ProductionConfig
}
