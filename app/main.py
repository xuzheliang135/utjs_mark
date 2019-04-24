from flask import redirect, url_for

from app import create_app, register_blueprint
from model.base import db

app = create_app()
register_blueprint(app)
db.create_all(app=app)


@app.route('/')
def index():
    return redirect(url_for('web.index'))


if __name__ == '__main__':
    app.run()
