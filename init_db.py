import os
import traceback
import sys
import psycopg2

sys.path.append(os.path.join(os.path.dirname(os.path.abspath("__file__")), "solucion-victoria"))
import config

# Se definen los parámetros de conexión a la BD con base en el ambiente (Dev/Prod)
def init_db():
    try:
        if 'DBNAME_DEV' not in os.environ:
            database=config.ProductionConfig.DBNAME
            user=config.ProductionConfig.DBUSER
            password=config.ProductionConfig.DBPASS
            host=config.ProductionConfig.DBHOST
            port=config.ProductionConfig.DBPORT
        else:
            database=config.DevelopmentConfig.DBNAME
            user=config.DevelopmentConfig.DBUSER
            password=config.DevelopmentConfig.DBPASS
            host=config.DevelopmentConfig.DBHOST
            port=config.DevelopmentConfig.DBPORT

        conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
        cur = conn.cursor()

        # Se borran las tablas usuario, conversacion y agente
        cur.execute("DROP TABLE IF EXISTS usuario CASCADE;")
        cur.execute("DROP TABLE IF EXISTS agente CASCADE;")
        cur.execute("DROP TABLE IF EXISTS documento CASCADE;")
        cur.execute("DROP TABLE IF EXISTS conversacion CASCADE;")

        # Se crean las tablas con sus respectivos campos
        cur.execute("CREATE TABLE usuario (id_usuario uuid DEFAULT gen_random_uuid () PRIMARY KEY,"
                    "nombre_usuario varchar (100) NOT NULL,"
                    "correo_usuario varchar (100) NOT NULL,"
                    "hash_auth_usuario varchar (100) NOT NULL,"
                    "agentes_permitidos varchar (100) [],"
                    "fecha_usuario date DEFAULT CURRENT_TIMESTAMP);")
        
        cur.execute("CREATE TABLE agente (id_agente uuid DEFAULT gen_random_uuid () PRIMARY KEY,"
                    "nombre_agente varchar (100) NOT NULL,"
                    "configuracion text,"
                    "tipo varchar (100) NOT NULL,"
                    "fecha_agente date DEFAULT CURRENT_TIMESTAMP);")
        
        cur.execute("CREATE TABLE documento (id_documento uuid DEFAULT gen_random_uuid () PRIMARY KEY,"
                    "nombre_documento varchar (100) NOT NULL,"
                    "archivo json [],"
                    "fecha_carga date DEFAULT CURRENT_TIMESTAMP);")

        cur.execute("CREATE TABLE conversacion (id_conversacion uuid DEFAULT gen_random_uuid () PRIMARY KEY,"
                    "id_usuario uuid NOT NULL,"
                    "id_agente uuid NOT NULL,"
                    "id_documento uuid,"
                    "nombre_conversacion varchar (100) NOT NULL,"
                    "historico_conversacion text NOT NULL,"
                    "tags varchar (100) [],"
                    "fecha_conversacion date DEFAULT CURRENT_TIMESTAMP,"
                    "CONSTRAINT fk_usuario FOREIGN KEY(id_usuario) REFERENCES usuario(id_usuario) ON DELETE CASCADE,"
                    "CONSTRAINT fk_agente FOREIGN KEY(id_agente) REFERENCES agente(id_agente) ON DELETE CASCADE,"
                    "CONSTRAINT fk_documento FOREIGN KEY(id_documento) REFERENCES documento(id_documento) ON DELETE CASCADE);")
        
        # Se añaden los agentes actualmente desarrollados
        cur.execute("INSERT INTO agente (nombre_agente, configuracion, tipo) VALUES ('Agente Pruebas',"
                    "'Descripción del proposito y configuración del agente de pruebas para mostrar en el portal web de VictorIA.',"
                    "'General');")
        
        cur.execute("INSERT INTO agente (nombre_agente, configuracion, tipo) VALUES ('Agente Azure',"
                    "'Un asesor de ventas que orienta al cliente sobre características y precios de máquinas virtuales de Azure según sus necesidades.',"
                    "'General');")
        
        cur.execute("INSERT INTO agente (nombre_agente, configuracion, tipo) VALUES ('Agente Licitaciones',"
                    "'Un asistente legal que ayuda a los usuarios a estudiar, analizar y resumir documentos de procesos licitatorios para encontrar infromación relevante y responder preguntas sobre estos.',"
                    "'RAG');")
        
        conn.commit()
        cur.close()
        conn.close()
    
    except:
        print(traceback.format_exc())
        print("No hemos podido crear la BD. Intenta de nuevo")

if __name__ == "__main__":
    init_db()
