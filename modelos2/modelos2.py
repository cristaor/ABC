from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
import datetime

db = SQLAlchemy()


class ValidatorLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.String(30))
    uuid = db.Column(db.String(60))
    instancia = db.Column(db.Numeric)
    payload = db.Column(db.String(256))
