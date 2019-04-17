from flask import current_app

from model.vote import VoteEvent


def refresh_control_info():
    res = VoteEvent.query.filter_by(is_active=True).first()
    if res:
        current_app.config['EVENT_ID'] = res.event_id
        current_app.config['LECTURE_TEAM'] = res.lecture_team
        current_app.config['VOTE_TEAM'] = res.vote_team
    else:
        current_app.config.from_pyfile('settings.py')
