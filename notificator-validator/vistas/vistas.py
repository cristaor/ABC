import os
from http import client
from multiprocessing import Event
from flask import request
from random import randint

from modelos.modelos import Notification, NotificationSchema
from modelos import db
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
import datetime
from celery import Celery
import enum
import json


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

class ReceivedNotificationRequestEvent:
    id: str
    date_event: datetime
    client_id: str
    location_id: str
    sensor_type : SensorType
    event_type: EventType
    instance: str

celery_app = Celery(__name__, broker = 'redis://localhost:6379/0')

notification_schema = NotificationSchema()

class VistaNotification(Resource):

    def post(self):
        
        return {"msg": "Reporte generado correctamente"}
    