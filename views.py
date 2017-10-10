import json

from models import User
from utils import json_response, redirect, render_template


def index(request):
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = render_template('index.html')
    response = header + '\r\n' + body
    return response.encode('utf-8')


def error(request, error_code=404):
    e = {
        404: b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>'
    }
    return e.get(error_code)


def login(request):
    if request.method == 'GET':
        header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
        body = render_template('login.html')
        response = header + '\r\n' + body
        return response.encode('utf-8')
    if request.method == 'POST':
        return redirect('/')


def register(request):
    if request.method == 'GET':
        header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
        body = render_template('register.html')
        response = header + '\r\n' + body
        return response.encode('utf-8')
    if request.method == 'POST':
        form = request.form_dict
        user = User(form['username'], form['password'])
        user.save()
        return redirect('/')


def static(request):
    file_name = request.query_dict.get('file_name', '')
    with open('static/{file_name}'.format(file_name=file_name), 'rb') as fin:
        header = b'HTTP/1.1 200 OK\r\n\r\n'
        body = fin.read()
        return header + body


def api_all(request):
    users = User.all()
    data = []
    for user in users:
        data.append(user.__dict__)
    return json_response(json.dumps(data))


def api_add(request):
    json_data = json.loads('{"username": "abc","password_hash": 456}')
    user = User(json_data['username'], json_data['password_hash'])
    user.save()
    return json_response('{"username": "abc","password_hash": 456}')


views_dict = {
    '/': index,
    '/login': login,
    '/register': register,
    '/static': static,
    '/api/all': api_all,
    '/api/add': api_add,
}
