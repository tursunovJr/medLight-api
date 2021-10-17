from flask import request
from flask_restful import Resource, abort
from marshmallow import ValidationError

from api.urls.fields import patients_info_schema, doctors_info_schema, services_info_schema, records_info_schema, \
    record_info_schema
from api.urls.models import Patient, Record, Doctor, Service
from api.urls.parsers import PatientSchema, RecordSchema, DoctorSchema, ServiceSchema
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
    def patch(patient_uuid):
        """Обновить информацию о пациенте по uuid"""
        if db.session.query(Patient).filter(Patient.uuid.like(str(patient_uuid))) \
                .one_or_none() is None:
            abort(404, message="Patient with uuid={} not found"
                  .format(patient_uuid))
        try:
            args = request.json
        except ValidationError as error:
            return make_response(400, message="Bad JSON format")

        patient = db.session.query(Patient).filter(Patient.uuid.like(str(patient_uuid))).one()
        for key in args:
            if args[key] is not None:
                setattr(patient, key, args[key])
        try:
            db.session.commit()
        except exc.SQLAlchemyError:
            db.session.rollback()
            return make_response(500, message="Database commit error")

        return make_empty(200)

    @staticmethod
    def post(patient_uuid):
        "Создать запись для пациента"
        if db.session.query(Patient).filter(Patient.uuid.like(str(patient_uuid))) \
                .one_or_none() is None:
            abort(404, message="Patient with uuid={} not found"
                  .format(patient_uuid))
        try:
            args = RecordSchema().load(request.json)
            args['patient_uuid'] = str(patient_uuid)
            # print(args['used_services'])
        except ValidationError as error:
            return make_response(400, message="Bad JSON format")
        record = Record(**args)
        try:
            db.session.add(record)
        except exc.SQLAlchemyError:
            db.session.rollback()
            return make_response(500, message="Database add error")

        try:
            db.session.commit()
        except exc.SQLAlchemyError:
            db.session.rollback()
            return make_response(500, message="Database commit error")

        return make_empty(201)


class Doctors(Resource):
    @staticmethod
    def post():
        """Создать нового врача"""
        try:
            args = DoctorSchema().load(request.json)
        except ValidationError as error:
            return make_response(400, message="Bad JSON format")
        doctor = Doctor(**args)
        try:
            db.session.add(doctor)
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
        """Получить список всех врачей"""
        doctors = db.session.query(Doctor).all()
        return make_response(200, doctor=doctors_info_schema.dump(doctors))


class DoctorAction(Resource):
    @staticmethod
    def delete(doctor_uuid):
        """Удалить врача по uuid"""
        if db.session.query(Doctor).filter(Doctor.uuid.like(str(doctor_uuid)))\
                .one_or_none() is None:
            abort(404, message="Doctor with uuid={} not found"
                  .format(doctor_uuid))

        doctor = db.session.query(Doctor).filter(Doctor.uuid.like(str(doctor_uuid))).one()
        try:
            db.session.delete(doctor)
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
    def patch(doctor_uuid):
        """Обновить информацию о враче по uuid"""
        if db.session.query(Doctor).filter(Doctor.uuid.like(str(doctor_uuid))) \
                .one_or_none() is None:
            abort(404, message="Doctor with uuid={} not found"
                  .format(doctor_uuid))
        try:
            args = request.json
        except ValidationError as error:
            return make_response(400, message="Bad JSON format")

        doctor = db.session.query(Doctor).filter(Doctor.uuid.like(str(doctor_uuid))).one()
        for key in args:
            if args[key] is not None:
                setattr(doctor, key, args[key])
        try:
            db.session.commit()
        except exc.SQLAlchemyError:
            db.session.rollback()
            return make_response(500, message="Database commit error")

        return make_empty(200)


class Services(Resource):
    @staticmethod
    def post():
        """Создать новую услугу"""
        try:
            args = ServiceSchema().load(request.json)
        except ValidationError as error:
            return make_response(400, message="Bad JSON format")
        service = Service(**args)
        try:
            db.session.add(service)
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
        """Получить список всех услуг"""
        services = db.session.query(Service).all()
        return make_response(200, service=services_info_schema.dump(services))


class ServiceAction(Resource):
    @staticmethod
    def delete(service_uuid):
        """Удалить услугу по id"""
        if db.session.query(Service).filter(Service.uuid.like(str(service_uuid)))\
                .one_or_none() is None:
            abort(404, message="Service with uuid={} not found"
                  .format(service_uuid))

        service = db.session.query(Service).filter(Service.uuid.like(str(service_uuid))).one()
        try:
            db.session.delete(service)
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
    def patch(service_uuid):
        """Обновить информацию о услуге по id"""
        if db.session.query(Service).filter(Service.uuid.like(str(service_uuid))) \
                .one_or_none() is None:
            abort(404, message="Service with uuid={} not found"
                  .format(service_uuid))
        try:
            args = request.json
        except ValidationError as error:
            return make_response(400, message="Bad JSON format")

        service = db.session.query(Service).filter(Service.uuid.like(str(service_uuid))).one()
        for key in args:
            if args[key] is not None:
                setattr(service, key, args[key])
        try:
            db.session.commit()
        except exc.SQLAlchemyError:
            db.session.rollback()
            return make_response(500, message="Database commit error")

        return make_empty(200)


class Records(Resource):
    @staticmethod
    def get():
        """Получить список всех записей пациентов у врача"""
        records = db.session.query(Record).all()
        return make_response(200, records=records_info_schema.dump(records))


class RecordAction(Resource):
    @staticmethod
    def get(record_uuid):
        """Получить запись по uuid"""
        if db.session.query(Record).filter(Record.uuid.like(str(record_uuid))) \
                .one_or_none() is None:
            abort(404, message="Record with uuid={} not found"
                  .format(record_uuid))
        record = db.session.query(Record).filter(Record.uuid.like(str(record_uuid))).one()
        return make_response(200, **record_info_schema.dump(record))

    @staticmethod
    def delete(record_uuid):
        """Удалить запись по uuid"""
        if db.session.query(Service).filter(Service.uuid.like(str(record_uuid))) \
                .one_or_none() is None:
            abort(404, message="Service with uuid={} not found"
                  .format(record_uuid))

        record = db.session.query(Record).filter(Record.uuid.like(str(record_uuid))).one()
        try:
            db.session.delete(record)
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
    def patch(record_uuid):
        """Обновить информацию о записи по uuid"""
        if db.session.query(Record).filter(Record.uuid.like(str(record_uuid))) \
                .one_or_none() is None:
            abort(404, message="Record with uuid={} not found"
                  .format(record_uuid))
        try:
            args = request.json
        except ValidationError as error:
            return make_response(400, message="Bad JSON format")

        record = db.session.query(Record).filter(Record.uuid.like(str(record_uuid))).one()
        for key in args:
            if args[key] is not None:
                setattr(record, key, args[key])
        try:
            db.session.commit()
        except exc.SQLAlchemyError:
            db.session.rollback()
            return make_response(500, message="Database commit error")

        return make_empty(200)