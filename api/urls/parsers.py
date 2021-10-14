from marshmallow import Schema, fields


class PatientSchema(Schema):
    name = fields.String(attribute="name", required=True)
    phone = fields.String(attribute="phone", required=True)
    birthday = fields.Date(attribute="birthday", format="iso8601",
                               required=True)