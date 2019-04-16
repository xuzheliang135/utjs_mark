from flask_login import login_user, login_required, current_user, logout_user

from model.base import db
from web.form.accountForm import LoginForm, SignUpForm
from . import web
from model.user import User
from flask import render_template, request, flash, redirect, url_for


@web.route('/log_in/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            next_url = request.args.get('next')
            if not next_url or not next_url.startswith('/'):
                next_url = url_for('web.index')
            return redirect(next_url)
        else:
            flash('账号不存在或密码错误', category='login_error')
    return render_template('login.html', form=form)


@web.route('/login_test/')
@login_required
def must_be_logined():
    return 'ok'


@web.route('/sign_up/', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm(request.form)
    if request.method == 'POST' and form.validate():
        with db.auto_commit():
            user = User()
            user.set_attrs(form.data)
            db.session.add(user)
            login_user(user)
        return redirect(url_for('web.login'))
    return redirect(url_for('web.score'))


@web.route('/log_out/')
def log_out():
    logout_user()
    return redirect(url_for('web.index'))
