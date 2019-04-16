from . import create_app, register_blueprint
from model.base import db
app = create_app()
register_blueprint(app)
db.create_all(app=app)
if __name__ == '__main__':
    app.run()
