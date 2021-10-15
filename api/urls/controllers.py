from flask import request
from flask_restful import Resource, abort, url_for
from marshmallow import ValidationError

from api.urls.fields import patients_info_schema, patient_info_schema, PatientInfoSchema
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

    @staticmethod
    def get():
        """Получить список всех пациентов"""
        patients = db.session.query(Patient).all()
        return make_response(200, patients=patients_info_schema.dump(patients))


class PatientAction(Resource):
    @staticmethod
    def delete(patient_uuid):
        """Удалить пациента по uuid"""
        if db.session.query(Patient).filter(Patient.uuid.like(str(patient_uuid)))\
                .one_or_none() is None:
            abort(404, message="Patient with uuid={} not found"
                  .format(patient_uuid))

        patient = db.session.query(Patient).filter(Patient.uuid.like(str(patient_uuid))).one()
        try:
            db.session.delete(patient)
        except exc.SQLAlchemyError:
            db.session.rollback()
            return make_response(500, message="Database delete error")

        try:
            db.session.commit()
        except exc.SQLAlchemyError:
            db.session.rollback()
            return make_response(500, message="Database commit error")

        return make_empty(200)

    @staticmethod
    def put(patient_uuid):
        """Обновить информацию о пациенте по uuid"""
        if db.session.query(Patient).filter(Patient.uuid.like(str(patient_uuid))) \
                .one_or_none() is None:
            abort(404, message="Patient with uuid={} not found"
                  .format(patient_uuid))
        try:
            # args = PatientSchema().load(request.json)
            args = request.json
            print("ARGS: ", args)
        except ValidationError as error:
            return make_response(400, message="Bad JSON format")

        # patient = db.session.query(Patient).filter(Patient.uuid.like(str(patient_uuid))).one()
        # try:
        #     db.session.delete(patient)
        # except exc.SQLAlchemyError:
        #     db.session.rollback()
        #     return make_response(500, message="Database delete error")
        #
        # try:
        #     db.session.commit()
        # except exc.SQLAlchemyError:
        #     db.session.rollback()
        #     return make_response(500, message="Database commit error")

        return make_empty(200)
