from flask import flash, redirect, render_template, request, session, url_for

from apps.auth import auth_blueprint
from apps.auth.models import User


def current_user():
    user_id = session.get('id', None)
    if user_id:
        return User.find_by(id=user_id)[0]
    return None


@auth_blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form['username']
        user = User.find_by(username=username)[0]
        if user and user.verify_password(request.form['password']):
            flash('登陆成功')
            session['id'] = user.id
            return redirect(url_for('home.index'))
        flash('登陆失败')
        return redirect(url_for('auth.login'))


@auth_blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.new(username, password)
        user.save()
        return redirect(url_for('auth.login'))


@auth_blueprint.route('/logout/')
def logout():
    session.pop('id')
    return redirect(url_for('auth.login'))
