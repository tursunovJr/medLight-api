from flask import Blueprint, json
from flask_restful import Api
from werkzeug.exceptions import HTTPException
from api.urls.controllers import Patients


api_urls_bp = Blueprint("api", __name__)
api_urls = Api(api_urls_bp)

# Add resources
api_urls.add_resource(Patients, "/patients")


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
