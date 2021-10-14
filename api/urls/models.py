from extensions import db
from uuid import uuid4


class Patient(db.Model):
    uuid = db.Column(db.String(36), primary_key=True,
                     default=lambda: str(uuid4()))
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(9), nullable=False)
    birthday = db.Column(db.Date, nullable=False)

    # def __repr__(self):
    #     return "<Patient: name={}, phone={}, birthday=\"{}\">\n"\
    #         .format(self.name, self.phone, self.birthday)
