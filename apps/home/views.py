from time import time

from flask import redirect, render_template, request, url_for

from apps.auth.views import current_user
from apps.home import home_blueprint
from apps.home.models import Topic, Comment


@home_blueprint.route('/', methods=['GET', 'POST'])
def index():
    user = current_user()
    if request.method == 'GET':
        topic_list = Topic.find_all()
        return render_template('index.html', user=user, topic_list=topic_list)
    if request.method == 'POST':
        Topic(int(time()), request.form['topic'], user.id).save()
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
