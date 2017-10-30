from flask_script import Manager

from config import Config
from apps import create_app, db
from apps.models import User

app = create_app(Config)
manager = Manager(app)


@manager.shell
def make_shell_context():
    return {
        'app': app,
        'db': db,
        'User': User,
    }


if __name__ == '__main__':
    manager.run()
