from flask import Flask

from apps.auth import auth_blueprint
from apps.home import home_blueprint


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(home_blueprint)
    return app
