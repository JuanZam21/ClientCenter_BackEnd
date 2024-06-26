import datetime
from . import db
from sqlalchemy import Column, Integer, String, Date, DECIMAL, ForeignKey, TIMESTAMP, TEXT

class User(db.Model):
    __tablename__ = 'Persona'

    id = db.Column(db.String(), primary_key=True)
    nombre = db.Column(db.String(50))
    apellido = db.Column(db.String(50))
    documento_identidad = db.Column(db.String(50))
    fecha_nacimiento = db.Column(db.Date)
    direccion = db.Column(db.String(100))
    correo_electronico = db.Column(db.String(50))
    telefono = db.Column(db.String(20))
    contrasena = db.Column(db.String(100))

class Sucursales(db.Model):
    __tablename__ = 'Sucursales'
    
    id_sucursal = db.Column(db.String(50), primary_key=True)
    nombre_sucursal = db.Column(db.String(50))
    ciudad = db.Column(db.String(20))
    departamento = db.Column(db.String(30))
    pais = db.Column(db.String(30))
    direccion = db.Column(db.String(100))
    telefono = db.Column(db.String(20))

class Credit(db.Model):
    __tablename__ = 'Creditos'
   
    id_credito = db.Column(db.String(50), primary_key=True)
    id_persona = db.Column(db.String(50), db.ForeignKey('Persona.id'))
    monto_original = db.Column(db.Numeric(10, 2))
    saldo_pendiente = db.Column(db.Numeric(10, 2))
    tasa_interes = db.Column(db.Numeric(5, 2))
    fecha_inicio = db.Column(db.Date)
    fecha_finalizacion = db.Column(db.Date)
    tipo_credito = db.Column(db.String(50))
    estado_credito = db.Column(db.String(50))

class Accounts(db.Model):
    __tablename__ = 'Cuentas'

    id_cuenta = db.Column(db.String(50), primary_key=True)
    id_persona = db.Column(db.String(50), db.ForeignKey('Persona.id'))
    id_tipo_cuenta = db.Column(db.String(50))
    saldo_actual = db.Column(db.Numeric(10, 2))
    moneda = db.Column(db.String(10))
    fecha_apertura = db.Column(db.Date)
    fecha_cierre = db.Column(db.Date)
    estado_cuenta = db.Column(db.String(50))
    beneficios = db.Column(db.String(200))

class Account_type(db.Model):
    __tablename__ = 'Tipo_cuenta'
    
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50))


class Cards(db.Model):
    __tablename__ = 'Tarjetas'

    id_tarjeta = Column(Integer, primary_key=True)
    id_persona = Column(Integer, ForeignKey('persona.id'))
    id_tipo_tarjeta = Column(Integer, ForeignKey('Tipo_tarjeta.id'))
    numero_tarjeta = Column(String(16))
    ultimos_digitos = Column(String(50))
    nombre_titular = Column(String(50))
    fecha_emision = Column(Date)
    fecha_vencimiento = Column(Date)
    fecha_corte = Column(Date)
    cupo_total = Column(DECIMAL(10, 2))
    cupo_disponible = Column(DECIMAL(10, 2))
    saldo_actual = Column(DECIMAL(10, 2))
    tasa_interes = Column(DECIMAL(5, 2))
    estado_tarjeta = Column(String(50))
    cvv = Column(String(3))
    pago_minimo = Column(DECIMAL(10, 2))
    pago_total = Column(DECIMAL(10, 2))
    pago_anticipado = Column(DECIMAL(10, 2))
    programa_puntos = Column(String(50))


class Card_type(db.Model):
    __tablename__ = 'Tipo_tarjeta'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))

class Transactions(db.Model):
    __tablename__ = 'Transacciones'

    id_transaccion = Column(Integer, primary_key=True)
    id_persona = Column(Integer, ForeignKey('persona.id'))
    id_tipo_transaccion = Column(String(50))
    monto = Column(DECIMAL(10, 2))
    fecha_transaccion = Column(TIMESTAMP)
    descripcion = Column(TEXT)

class Transaction_type(db.Model):
    __tablename__ = 'Tipo_transaccion'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))

class History(db.Model):
    __tablename__ = 'Historial_Atencion_Cliente'

    id_atencion = Column(Integer, primary_key=True)
    id_cliente = Column(Integer, ForeignKey('Persona.id'))
    id_empleado = Column(Integer, ForeignKey('Persona.id'))
    fecha_atencion = Column(TIMESTAMP, default=datetime.date.today)
    tipo_atencion = Column(String(50))
    descripcion = Column(TEXT)
    categoria = Column(TEXT)
    estado = Column(TEXT)
    duracion_llamada = Column(Integer)

class Role(db.Model):
    __tablename__ = 'Rol'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(50))

class UserRole(db.Model):
    __tablename__ = 'Persona_role'

    id = Column(Integer, primary_key=True)
    id_persona = Column(String(50))
    id_rol = Column(String(50))