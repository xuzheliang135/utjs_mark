from flask import render_template, request, flash, redirect, url_for, current_app
from flask_login import login_user, login_required, logout_user, current_user

from app.model.base import db
from app.model.user import User
from app.web.form.accountForm import LoginForm, SignUpForm, ResetPasswordForm
from . import web


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
    current_app.config.from_pyfile('settings.py')
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
        return redirect(url_for('web.index'))
    return render_template('sign_up.html', form=form)


@web.route('/reset_password/', methods=['GET', 'POST'])
@login_required
def reset_password():
    form = ResetPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        with db.auto_commit():
            user = User.query.filter_by(username=current_user.username).first()
            if user.check_password(form.old_password.data):
                user.password = form.password.data
                db.session.add(user)
                logout_user()
                return redirect(url_for('web.login'))
        flash("原密码不对！请检查后再次输入")
    return render_template('reset_password.html', form=form)


@web.route('/log_out/')
def log_out():
    logout_user()
    return redirect(url_for('web.index'))
