

import sqlalchemy as db

import enum
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
import datetime

class SensorType(enum.Enum):
    TEMPERATURA = 1
    HUMEDAD = 2
    CONCENTRACION = 3
    INCENDIO = 4
    MOVIMIENTO = 5
    SIGNOS = 6
    PANICO = 7

class EventType(enum.Enum):
    MEDICION = 1
    ADVERTENCIA = 2
    ALARMA = 3

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date_event = db.Column(db.String(10))
    message = db.Column(db.String(250))
    instance = db.Column(db.Integer)

    # Representación del objeto
    def __repr__(self) -> str:
        return "{}-{}-{}-{}".format(self.id, self.date_event, self.message, self.instance)

class NotificationSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = Notification
         load_instance = True