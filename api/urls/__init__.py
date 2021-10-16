from flask import Blueprint, json
from flask_restful import Api
from werkzeug.exceptions import HTTPException
from api.urls.controllers import Patients, PatientAction, Doctors, DoctorAction

api_urls_bp = Blueprint("api", __name__)
api_urls = Api(api_urls_bp)

# Add resources
api_urls.add_resource(Patients, "/patients")
api_urls.add_resource(PatientAction, "/patients/<uuid:patient_uuid>")
api_urls.add_resource(Doctors, "/doctors")
api_urls.add_resource(DoctorAction, "/doctors/<uuid:doctor_uuid>")

# JSON format for error
@api_urls_bp.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response
