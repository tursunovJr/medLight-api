from marshmallow import Schema, fields


class UserSchema(Schema):
    username = fields.String(attribute="username", required=True)
    password = fields.String(attribute="password", required=True)


class PatientSchema(Schema):
    name = fields.String(attribute="name", required=True)
    phone = fields.String(attribute="phone", required=True)
    birthday = fields.Date(attribute="birthday", format="iso8601",
                           required=True)


class DoctorSchema(Schema):
    name = fields.String(attribute="name", required=True)
    phone = fields.String(attribute="phone", required=True)
    speciality = fields.String(attribute="speciality", required=True)
    qualification = fields.String(attribute="qualification", required=True)


class ServiceSchema(Schema):
    name = fields.String(attribute="name", required=True)
    price = fields.Integer(attribute="price", required=True)


class RecordSchema(Schema):
    # patient_uuid = fields.String(attribute="patient_uuid", required=True)
    doctor_uuid = fields.String(attribute="doctor_uuid", required=True)
    date = fields.DateTime(attribute="date", required=True)
    used_services = fields.String(attribute="used_services", required=True)
    disease = fields.String(attribute="disease", required=True)
    discharge = fields.String(attribute="discharge", required=True)
    payment_status = fields.Boolean(attribute="payment_status", required=True)
    sum = fields.Integer(attribute="sum", required=True)
