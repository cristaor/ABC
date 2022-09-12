cd tareas
pwd
pip install celery
celery -A tareas worker -l info -Q queue.notification.requested