import os
from time import time

from flask import redirect, render_template, request, url_for, jsonify
from werkzeug import secure_filename

from apps.auth.views import current_user
from apps.home import home_blueprint
from apps.home.utils import check_upload
from apps.home.models import Topic, Comment, Board


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
    filename = secure_filename(avatar_file.filename)
    if check_upload(filename):
        print(filename)
        path = os.path.join(os.getcwd(), 'uploads/avatars/' + filename)
        avatar_file.save(path)
    return redirect(url_for('home.index'))
