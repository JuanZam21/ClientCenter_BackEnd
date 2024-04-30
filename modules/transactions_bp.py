import json
from sqlalchemy.orm.exc import NoResultFound
from .. import db
from flask import Blueprint, jsonify, request
from collections import defaultdict
from flasgger import swag_from
from ..models import User, Cards, Card_type

cards_bp = Blueprint('cards_bp', __name__)

# Consulta de preguntas tarjeats
@cards_bp.route('/api/tarjeta/questions')
def question():
    return jsonify(
        {
  "data": [
    {
      "label": "Fecha de emision",
      "name": "fechaEmision"
    },
    {
      "label": "Fecha de vencimiento",
      "name": "fechaVencimiento"
    },
    {
      "label": "Fecha de corte",
      "name": "fechaCorte"
    },
    {
      "label": "Cupo total",
      "name": "cupoTotal"
    },
    {
      "label": "Tasa de interes",
      "name": "tasaInteres"
    },
    {
      "label": "Estado",
      "name": "estado"
    },
    {
      "label": "Pago minimo",
      "name": "pagoMinimo"
    },
    {
      "label": "Pago total",
      "name": "pagoTotal"
    },
    {
      "label": "Programa de puntos",
      "name": "programaPuntos"
    }
  ],
  "success": True,
  "message": "Preguntas encontradas"
}),200
