from flask import Flask
from flask_migrate import Migrate, Manager, MigrateCommand

from model.base import db

app = Flask(__name__)
app.config.from_pyfile('secure.py')
app.config.from_pyfile('settings.py')

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
