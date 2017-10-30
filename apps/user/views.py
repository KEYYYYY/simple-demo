from flask import jsonify, redirect, render_template, request, url_for

from apps import db
from apps.models import User
from apps.user import user_blueprint


@user_blueprint.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('user/register.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User()
        user.username = username
        user.password = password
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user.register'))


@user_blueprint.route('/verify_username/', methods=['POST'])
def verify_username():
    data = request.form
    user = User.query.filter_by(username=data['username']).first()
    if user:
        return jsonify({
            'status': True
        })
    return jsonify({
        'status': False
    })
