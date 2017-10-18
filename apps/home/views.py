import os
from time import time

from flask import (current_app, jsonify, redirect, render_template, request,
                   url_for, send_from_directory)
from werkzeug import secure_filename

from apps.auth.views import current_user
from apps.home import home_blueprint
from apps.home.models import Board, Comment, Topic
from apps.home.utils import check_upload


@home_blueprint.route('/', methods=['GET', 'POST'])
def index():
    user = current_user()
    if request.method == 'GET':
        topic_list = Topic.find_all()
        return render_template('index.html', user=user, topic_list=topic_list)
    if request.method == 'POST':
        Topic(
            int(time()),
            request.form['topic'],
            user.id,
            request.form['board']
        ).save()
        return redirect(url_for('home.index'))


@home_blueprint.route('/detail/<int:id>/', methods=['GET', 'POST'])
def detail(id):
    topic = Topic.find_by(id=id)
    if request.method == 'GET':
        comments = Comment.find_by(topic_id=topic[0].id)
        return render_template(
            'detail.html',
            topic=topic[0],
            comments=comments
        )
    if request.method == 'POST':
        content = request.form['content']
        Comment(int(time()), topic[0].id, current_user().id, content).save()
        return redirect(url_for('home.detail', id=topic[0].id))


@home_blueprint.route('/api/topics/<int:board_id>')
def topic(board_id):
    topic_list = Board.find_by(id=str(board_id))[0].topics()
    return jsonify({
        'topics': [topic.to_json() for topic in topic_list],
    })


@home_blueprint.route('/upload/', methods=['POST'])
def upload_avatar():
    avatar_file = request.files['avatar']
    # 转义文件名使其安全
    file_name = secure_filename(avatar_file.filename)
    # 判断文件格式是否符合要求
    if check_upload(file_name):
        path = os.path.join(current_app.config['UPLOAD_FOLDER'], file_name)
        avatar_file.save(path)
        user = current_user()
        user.avatar = file_name
        user.save()
    return redirect(url_for('home.index'))


@home_blueprint.route('/avatars/<file_name>/')
def avatar(file_name):
    with open(current_app.config['UPLOAD_FOLDER'] + file_name, 'rb') as f:
        return f.read()
