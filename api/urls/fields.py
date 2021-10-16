from marshmallow import fields, Schema


class PatientInfoSchema(Schema):
    uuid = fields.String(attribute="uuid")
    name = fields.String(attribute="name", required=True)
    phone = fields.String(attribute="phone", required=True)
    birthday = fields.Date(attribute="birthday", format="iso8601",
                           required=True)


class DoctorInfoSchema(Schema):
    uuid = fields.String(attribute="uuid")
    name = fields.String(attribute="name", required=True)
    phone = fields.String(attribute="phone", required=True)
    speciality = fields.String(attribute="speciality", required=True)
    qualification = fields.String(attribute="qualification", required=True)


patients_info_schema = PatientInfoSchema(many=True)
doctors_info_schema = DoctorInfoSchema(many=True)