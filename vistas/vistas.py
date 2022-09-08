from flask import request
from flask_jwt_extended import jwt_required, create_access_token
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from modelos import db, Central, CentralSchema, Cliente, ClienteSchema
import re
import json
import numbers

central_schema = CentralSchema()
cliente_schema = ClienteSchema()
"""carrera_schema = CarreraSchema()
competidor_schema = CompetidorSchema()
usuario_schema = UsuarioSchema()
reporte_schema = ReporteSchema()"""
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

class VistaCentral(Resource):
    #@jwt_required()
    def post(self):
        nueva_central = Central(nombre=request.json["nombre"], direccion=request.json["direccion"], telefono=request.json["telefono"], regional=request.json["regional"], pais=request.json["pais"], ciudad=request.json["ciudad"])
        #print(json.dumps(request.json))
        db.session.add(nueva_central)
        db.session.commit()
        return central_schema.dump(nueva_central)

    def get(self):
        return ([central_schema.dumps(central) for central in  Central.query.all()])

class VistaClientesCentral(Resource):

    def post(self, id_central):
        central = Central.query.get_or_404(id_central)

        if "id_cliente" in request.json.keys():

            nuevo_cliente = Cliente.query.get(request.json["id_cliente"])
            if nuevo_cliente is not None:
                central.clientes.append(nuevo_cliente)
                db.session.commit()
            else:
                return 'Cliente erróneo',404
        else:
            nuevo_cliente = Cliente(nombre=request.json["nombre"], direccion=request.json["direccion"], telefono=request.json["telefono"], email=request.json["email"], usuario=request.json["usuario"], clave=request.json["clave"],activo=request.json["activo"])
            central.clientes.append(nuevo_cliente)
        db.session.commit()
        return cliente_schema.dump(nuevo_cliente)

    def get(self, id_central):
        central = Central.query.get_or_404(id_central)
        return [cliente_schema.dump(ca) for ca in central.clientes]
