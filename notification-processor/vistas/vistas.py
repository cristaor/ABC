import os
from http import client
from multiprocessing import Event
from typing import Tuple
from flask import request
from random import randint

from modelos.modelos import Notification, NotificationSchema
from modelos import db, FailType
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

celery_app = Celery(__name__, broker = 'redis://redis:6379/0')

@celery_app.task(name="registrar_log")
def publish_event(*args):
    pass

notification_schema = NotificationSchema()

class VistaNotification(Resource):

    def post(self):

        notification = Notification(extern_uuid = request.json["uuid"], 
                                    client_id=request.json["client_id"], 
                                    location_id=request.json["location_id"], 
                                    sensor_type=request.json["sensor_type"], 
                                    event_type=request.json["event_type"], 
                                    date_event =request.json["fecha_evento"])
        
        build_received_request_event(notification = notification, id = notification.extern_uuid, date_event =  notification.date_event, client_id =  notification.client_id, 
                                location_id = notification.location_id, sensor_type = SensorType[notification.sensor_type], event_type=EventType[notification.event_type])

        return {"msg": "Notificación recibida exitosamente"}




def should_inject_error(hash: int)->Tuple[bool, FailType]:

    if randint(0, 100) > 50 and hash % 3 == (int(os.environ.get('instance')) -1) :
        return (True, FailType.MENSAJE_ERRADO) if randint(0, 100) > 50 else (True, FailType.NO_ENVIADO)
    else:
        return (False, FailType.NONE)

def build_received_request_event(notification: Notification, id: str, date_event: datetime, client_id: str, 
                                location_id: str, sensor_type : SensorType, 
                                event_type: EventType)->None:

    event = ReceivedNotificationRequestEvent()
    event.id = id
    event.date_event = date_event

    event.location_id = location_id
    event.sensor_type = sensor_type
    event.event_type = event_type
    event.instance = os.environ.get('instance')

    must_fail, type_fail = should_inject_error(hash(notification.extern_uuid))

    


    if not must_fail:
        event.client_id = client_id
        args = ("event", json.dumps(event.__dict__, default=str))
        publish_event.apply_async(args=args, queue= 'queue.notification.requested')
    else:
        
        print("Alterando el payload para la solicitud {} desde la instancia {}".format(id, os.environ.get('instance')))
        notification.fail_type = type_fail.name
        db.session.add(notification)
        db.session.commit()

        if FailType.MENSAJE_ERRADO is type_fail:
            event.client_id = 222
            args = ("event", json.dumps(event.__dict__, default=str))
            publish_event.apply_async(args=args, queue= 'queue.notification.requested')
    
       
    