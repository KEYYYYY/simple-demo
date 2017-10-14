from config import DevConfig
from apps import create_app

app = create_app(DevConfig)

if __name__ == '__main__':
    app.run()
