# ABC

## Como correr el proyecto?
Para correr el projecto es necesario tener Docker instalado, se debe ejecutar el siguiente comando:´

 `` 
 docker compose up -d
 `` 
 
 Se deberan observar 4 microservicios desplegados y 2 servicios
 1. Redis
 2. Postgres
 3. Notification1
 4. Notification2
 5. Notification2
 6. API Gateway
 
 Despues de ver los servicios desplegados
 
 Se debe levantar el Validator, para esto se debe ejecutar 
 
 ## Construir el proyecto
 
```
 cd notificator-validator \n
 pip install -r requeriments.txt
```

## Desplegar el Validator
```
 cd tareas \n
 celery -A tareas worker -l info -Q queue.notification.requested
```
 
 ## Enviar pruebas
 ```
  cd gateway
  pip install -r requeriments.txt
  python notification_sender.py
 ```
 
