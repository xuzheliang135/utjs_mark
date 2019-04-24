from flask import Flask
from flask_admin import Admin
from flask_babelex import Babel
from flask_login import LoginManager

from admin_view_model import UserModelView, VoteEventModelView
from model.base import db

login_manager = LoginManager()


def create_app():
    from web.util.util import refresh_control_info

    app = Flask(__name__)
    app.config.from_pyfile('secure.py')
    app.config.from_pyfile('settings.py')
    # 注册SQLAlchemy
    db.init_app(app)

    # 注册login模块
    login_manager.init_app(app)
    login_manager.login_view = 'web.login'
    login_manager.login_message = '请先登录或注册'

    # 注册admin模块
    from model.user import User
    from model.vote import VoteEvent
    admin = Admin(app=app, name='后台管理系统', template_mode='bootstrap3')
    admin.add_view(UserModelView(User, db.session, name='用户管理'))
    admin.add_view(VoteEventModelView(VoteEvent, db.session, name='投票管理'))

    # 国际化
    babel = Babel()
    babel.init_app(app)

    # 刷新投票控制信息
    with app.app_context(): refresh_control_info()

    return app


def register_blueprint(app):
    from web import web
    app.register_blueprint(web, url_prefix='/web')
    # app.register_blueprint(web)
