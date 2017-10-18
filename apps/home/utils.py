from flask import current_app


def check_upload(filename):
    if '.' not in filename:
        return False
    if filename.split('.')[-1].lower() not in current_app.config['ALLOWED_EXTENSIONS']:
        return False
    return True
