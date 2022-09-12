from celery import Celery
import json
from sqlalchemy import text
import hashlib



import sqlalchemy as db



engine = db.create_engine(f'postgresql+psycopg2://postgres@localhost:5432/postgres')



engine.connect()

engine.execute(
        text(
        "CREATE TABLE IF NOT EXISTS notification_validador (id TEXT, date_event TEXT NOT NULL, message TEXT, instance TEXT)"
        )
    )
celery_app = Celery(__name__, broker='redis://localhost:6379/0')
#Asegurarnos que esta función pasará a través de la cola
@celery_app.task(name='registrar_log')
def registrar_log(event, payload: str):

    datos = json.loads(payload)
    print(datos)

    engine.execute(
        text(
        "insert into notification_validador values ('{}', '{}', '{}', '{}')".format(datos["id"], datos["date_event"], datos["client_id"], datos["instance"]))
    )

    #notification = Notification(id = datos["id"], date_event=datos["date_event"], message=datos, instance=datos["instance"])
    #db.session.add(notification)
    #db.session.commit()


    with open('logValidator.txt', 'a+') as file:
        file.write('{} - {}\n'.format(event, payload))