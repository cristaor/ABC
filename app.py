from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
import os
from modelos import db, SensorSchema, Sensor, TipoSensor, Central, CentralSchema, Cliente, ClienteSchema, Ubicacion, UbicacionSchema
from vistas import VistaCentral, VistaClientesCentral
"""from vistas import VistaApuestas, VistaApuesta, VistaSignIn, VistaLogIn, VistaCarrerasUsuario, \
    VistaCarrera, VistaTerminacionCarrera, VistaReporte,VistaHealthCheck"""
from faker import Faker
from faker.generator import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ABC.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.drop_all()
db.create_all()

cors = CORS(app)

api = Api(app)

api.add_resource(VistaCentral, '/central')
api.add_resource(VistaClientesCentral, '/central/<int:id_central>/clientes')
"""
api.add_resource(VistaHealthCheck, '/health')
api.add_resource(VistaSignIn, '/signin')
api.add_resource(VistaLogIn, '/login')
api.add_resource(VistaCarrerasUsuario, '/usuario/<int:id_usuario>/carreras')
api.add_resource(VistaCarrera, '/carrera/<int:id_carrera>')
api.add_resource(VistaApuestas, '/apuestas')
api.add_resource(VistaApuesta, '/apuesta/<int:id_apuesta>')
api.add_resource(VistaTerminacionCarrera, '/carrera/<int:id_competidor>/terminacion')
api.add_resource(VistaReporte, '/carrera/<int:id_carrera>/reporte')

jwt = JWTManager(app)
"""



with app.app_context():
    data_factory = Faker()
    #iniciar la serializacion
    central_schema = CentralSchema()
    #crear una central
    c= Central(nombre='Zona Norte', direccion='Calle 95 No 12-34', telefono='98765432', regional='Central', pais='Colombia', ciudad='Bogota')

    for i in range(10):
        nombre = data_factory.first_name() + " " + data_factory.last_name();
        direccion = data_factory.address()
        telefono = data_factory.random_int(3000000000, 35000000000)
        email=data_factory.ascii_safe_email()
        usuario = data_factory.word()
        clave=data_factory.password()

        #crear unos clientes
        cliente_schema = ClienteSchema()
        cl= Cliente(nombre=nombre, direccion=direccion, telefono=telefono, email=email, usuario=usuario, clave=clave,activo='S')
        #agregar los clientes a la central
        c.clientes.append(cl)


        #nueva ubicacion
        nombre2=data_factory.company()
        direccion2=data_factory.address()
        descripcion= data_factory.paragraph(nb_sentences=2);

        ub= Ubicacion (nombre=nombre2, direccion=direccion2,  pais='Colombia', ciudad='Bogota', descripcion=descripcion)
        cl.ubicaciones.append(ub)

        list1 = ['TEMPERATURA','HUMEDAD','CONCENTRACION','INCENDIO','MOVIMIENTO','SIGNOS','PANICO']

        sensor_tipo2=random.choice(list1)
        serial2=data_factory.bothify(text='????-########')
        marca2=data_factory.company()
        s = Sensor(serial=serial2, marca= marca2, tipo=sensor_tipo2)

        sensor_tipo2=random.choice(list1)
        serial2=data_factory.bothify(text='????-########')
        marca2=data_factory.company()
        s2 = Sensor(serial=serial2, marca= marca2, tipo=sensor_tipo2)
        ub.sensores.append(s)
        ub.sensores.append(s2)

    db.session.add(c)

    """

    sensor_schema = SensorSchema()
    s = Sensor(serial='MNS98746SX', marca='Samsung', tipo=TipoSensor.PANICO)
    s2 = Sensor(serial='ASFEFCXA', marca='Phillips', tipo=TipoSensor.MOVIMIENTO)
    ub.sensores.append(s)
    ub.sensores.append(s2)
"""
    db.session.commit()
    #convertir la consulta en Json
    #print([central_schema.dumps(central) for central in  Central.query.all()])
    print(Central.query.all()[0].clientes)
   # print([sensor_schema.dumps(sensor) for sensor in  Sensor.query.all()])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
