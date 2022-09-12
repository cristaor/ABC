from celery import Celery
import json
from sqlalchemy import text
import hashlib



import sqlalchemy as db

celery_app = Celery(__name__, broker='redis://localhost:6379/0')

engine = db.create_engine('sqlite:///notificationProcessor.db')
engine.connect()

engine.execute(
        text(
        "CREATE TABLE IF NOT EXISTS notification (id TEXT, date_event TEXT NOT NULL, message TEXT, instance TEXT)"
        )
    )

#Asegurarnos que esta función pasará a través de la cola
@celery_app.task(name='registrar_log')
def registrar_log(event, payload: str):

    datos = json.loads(payload)
    print(datos)

    engine.execute(
        text(
        "insert into notification values ('{}', '{}', '{}', '{}')".format(datos["id"], datos["date_event"], hashlib.md5(payload.encode('utf-8')).hexdigest(), datos["instance"]))
    )

    #notification = Notification(id = datos["id"], date_event=datos["date_event"], message=datos, instance=datos["instance"])
    #db.session.add(notification)
    #db.session.commit()


    with open('logValidator.txt', 'a+') as file:
        file.write('{} - {}\n'.format(event, payload))