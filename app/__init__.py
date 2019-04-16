from flask import Flask
from flask_login import LoginManager

from model.base import db

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('secure.py')
    app.config.from_pyfile('settings.py')
    # 注册SQLAlchemy
    db.init_app(app)

    # 注册login模块
    login_manager.init_app(app)
    login_manager.login_view = 'web.login'
    login_manager.login_message = '请先登录或注册'
    return app


def register_blueprint(app):
    from web import web
    # app.register_blueprint(web, url_prefix='/web')
    app.register_blueprint(web)
