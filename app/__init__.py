from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, IMAGES, configure_uploads

db = SQLAlchemy()
avatars = UploadSet('avatars', IMAGES)


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    configure_uploads(app, avatars)

    from app.user import user_blueprint
    app.register_blueprint(user_blueprint)
    return app
