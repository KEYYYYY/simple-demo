# from flask.config import Config


def check_upload(filename):
    if '.' not in filename:
        return False
    if filename.split('.')[-1].lower() not in {'png', 'jpg', 'jpeg', 'gif'}:
        return False
    return True
