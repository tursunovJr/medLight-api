from flask import Flask
import os

from api import UserLogIn

SECRET_KEY = os.urandom(32)
CONFIG_NAME_MAPPER = {
    "testing": "config.TestingConfig",
    "production": "config.ProductionConfig",
}


def create_app(config_name=None):
    app = Flask(__name__)

    if config_name is None:
        config_name = "production"

    app.config.from_object(CONFIG_NAME_MAPPER[config_name])
    app.config['SECRET_KEY'] = SECRET_KEY

    # Register extensions
    from extensions import db, cors, ma, login_manager
    db.init_app(app)
    cors.init_app(app)
    ma.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'api.userlogin'

    # Register Blueprints
    from api import api_bp
    app.register_blueprint(api_bp, url_prefix="/api/v1")
    return app
