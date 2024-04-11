from flask_login import UserMixin
import os, sys
import datetime
import uuid
from . import db

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey, CheckConstraint
import uuid

class Clientes(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.Date)

class Transacciones(db.Model):
    __tablename__ = 'transacciones'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cliente_id = db.Column(db.Integer, ForeignKey('clientes.id'), nullable=False)
    tipo_transaccion = db.Column(db.String(50))
    monto = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.Date)

class Saldos(db.Model):
    __tablename__ = 'saldos'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cliente_id = db.Column(db.Integer, ForeignKey('clientes.id'))
    tipo_cuenta = db.Column(db.String(100))
    saldo = db.Column(db.Numeric(10, 2))
    fecha_actualizacion = db.Column(db.DateTime)

class Informacion_Adicional(db.Model):
    __tablename__ = 'informacion_adicional'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cliente_id = db.Column(db.Integer, ForeignKey('clientes.id'))
    categoria = db.Column(db.String(50))
    detalle = db.Column(db.Text)
    db.Column(db.ARRAY(db.String(100)))  # Fix: Replace 'column' with 'db.Column'
    fecha_usuario = db.Column(db.Date, default=datetime.date.today)