from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column
from sqlalchemy import String, Integer
from model.base import Base
from app import login_manager


class User(UserMixin, Base):
    __tablename__ = 'user'

    username = Column('username', String(20), primary_key=True)
    name = Column('name', String(10))
    team_id = Column('team_id', Integer())
    _password = Column('password', String(100))

    def get_id(self):
        return self.username

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)


@login_manager.user_loader
def get_user(username):
    return User.query.get(username)
