from sqlalchemy import Column
from sqlalchemy import String, Integer, ForeignKey
from model.base import Base


class Vote(Base):
    __tablename__ = 'vote'

    voter = Column('voter', String(20), ForeignKey("user.username"), primary_key=True)
    lecturer = Column('lecturer', String(20), ForeignKey("user.username"), primary_key=True)
    content = Column('content', Integer())
    gesture = Column('gesture', Integer())
    voice = Column('voice', Integer())
