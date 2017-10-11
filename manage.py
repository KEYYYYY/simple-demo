from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)


def login_required(f):
    def decorator():
        if session.get('username'):
            return f()
        return redirect(url_for('login'))
    return decorator


@app.route('/')
@login_required
def index():
    username = session.get('username', '陌生人')
    return '<h1>{username}<h1>'.format(username=username)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'Tom' and password == '123':
            session['username'] = username
            return redirect('/')
        return redirect(url_for('login'))


@app.route('/logout')
@login_required
def logout():
    session.pop('username')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.debug = True
    app.secret_key = '763997136'
    app.run()
