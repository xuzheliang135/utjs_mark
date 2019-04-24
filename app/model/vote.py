from sqlalchemy import Column, Boolean
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.event import listens_for

from model.base import Base


class Vote(Base):
    __tablename__ = 'vote'

    voter = Column('voter', String(20), ForeignKey("user.username"), primary_key=True)
    lecturer = Column('lecturer', String(20), ForeignKey("user.username"), primary_key=True)
    content = Column('content', Integer())
    gesture = Column('gesture', Integer())
    voice = Column('voice', Integer())
    event_id = Column('event_id', Integer(), ForeignKey("vote_event.event_id"), primary_key=True)


class VoteTmp(Base):
    __tablename__ = 'votetmp'

    voter = Column('voter', String(20), ForeignKey("user.username"), primary_key=True)
    vote_target = Column('vote_target', String(20), ForeignKey("user.username"), primary_key=True)
    score = Column('score', Integer())
    event_id = Column('event_id', Integer(), ForeignKey("vote_event.event_id"), primary_key=True)


class VoteEvent(Base):
    __tablename__ = 'vote_event'
    event_id = Column('event_id', Integer(), primary_key=True, autoincrement=True)
    lecture_team = Column('lecture_team', Integer(), nullable=False)
    vote_team = Column('vote_team', Integer(), nullable=False)
    is_active = Column('is_active', Boolean(), default=False)


@listens_for(VoteEvent, "before_update")
def receive_before_update(mapper, connection, instance):
    if instance.is_active:
        from web.util.util import refresh_control_info
        connection.execute(
            f'update vote_event set is_active=false where is_active=true and event_id!={instance.event_id}')
        refresh_control_info()


@listens_for(VoteEvent, "before_insert")
def receive_before_insert(mapper, connection, instance):
    if instance.is_active:
        from web.util.util import refresh_control_info
        connection.execute('update vote_event set is_active=false where is_active=true')
        refresh_control_info()
        # todo:无法在回调函数中使用SQLAlchemy更改数据
