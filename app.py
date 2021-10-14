from flask import Flask


CONFIG_NAME_MAPPER = {
    "testing": "config.TestingConfig",
    "production": "config.ProductionConfig",
}


def create_app(config_name=None):
    app = Flask(__name__)

    if config_name is None:
        config_name = "production"

    app.config.from_object(CONFIG_NAME_MAPPER[config_name])

    # Register extensions
    from extensions import db, cors, ma
    db.init_app(app)
    cors.init_app(app)
    ma.init_app(app)

    # Register Blueprints
    from api.urls import api_urls_bp
    app.register_blueprint(api_urls_bp, url_prefix="/api/v1")
    return app
