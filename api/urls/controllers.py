from flask import request
from flask_restful import Resource, abort, url_for
from marshmallow import ValidationError

from api.urls.models import Patient
from api.urls.parsers import PatientSchema
from api.utils import make_response, make_empty
from extensions import db
from sqlalchemy import exc


class Patients(Resource):
    @staticmethod
    def post():
        """Создать нового пациента"""
        try:
            args = PatientSchema().load(request.json)
        except ValidationError as error:
            return make_response(400, message="Bad JSON format")
        patient = Patient(**args)
        try:
            db.session.add(patient)
        except exc.SQLAlchemyError:
            db.session.rollback()
            return make_response(500, message="Database add error")

        try:
            db.session.commit()
        except exc.SQLAlchemyError:
            db.session.rollback()
            return make_response(500, message="Database commit error")

        return make_empty(201)

