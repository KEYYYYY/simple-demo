from flask import (current_app, redirect, render_template, send_from_directory,
                   url_for)

from app import avatars, db
from app.models import User
from app.user import user_blueprint
from app.user.forms import UserForm
from app.user.utils import create_thumbnail


@user_blueprint.route('/', methods=['GET', 'POST'])
def index():
    user = User.query.first()
    if user.avatar:
        avatar_t_url = url_for('user.avatar', file_name=user.avatar_t)
    else:
        avatar_t_url = None
    user_form = UserForm()
    user_form.username.data = user.username
    if user_form.validate_on_submit():
        # 如果选择头像不为空就更新用户头像
        if user_form.avatar is not None:
            file_name = avatars.save(user_form.avatar.data)
            user.avatar = file_name
            file_name_t = create_thumbnail(file_name)
            user.avatar_t = file_name_t
        user.username = user_form.username.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user.index'))
    return render_template(
        'index.html',
        user_form=user_form,
        avatar_url=avatar_t_url
    )


@user_blueprint.route('/uploads/avatar/<file_name>')
def avatar(file_name):
    return send_from_directory(
        current_app.config['UPLOADED_AVATARS_DEST'],
        file_name,
        as_attachment=True,
    )
