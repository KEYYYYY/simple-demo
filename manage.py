from flask_script import Manager

from app import create_app, db
from config import Config
from app.models import User

app = create_app(Config)
manager = Manager(app)


@manager.shell
def create_shell_context():
    return {
        'app': app,
        'db': db,
        'User': User,
    }


if __name__ == '__main__':
    manager.run()
