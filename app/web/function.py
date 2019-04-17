from flask import render_template, request, current_app, abort, flash
from flask_login import login_required, current_user
from sqlalchemy import func

from model.base import db
from model.user import User
from model.vote import Vote
from web.form.accountForm import VoteForm
from . import web


def get_team_members(team_id):
    return User.query.filter_by(team_id=team_id).all()


@web.route('/vote/', methods=['GET', 'POST'])
@login_required
def vote_page():
    form = VoteForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(username=current_user.get_id()).first()
        if user.team_id != current_app.config['VOTE_TEAM']:
            flash('只有点评组才能投票哦', category='privilege_error')
            abort(403)
        vote = Vote.query.filter_by(voter=current_user.get_id(),
                                    lecturer=form.lecturer.data,
                                    event_id=current_app.config['EVENT_ID']).first()
        if not vote:
            vote = Vote()
        with db.auto_commit():
            vote.set_attrs(form.data)
            vote.voter = current_user.get_id()
            vote.event_id = current_app.config['EVENT_ID']
            db.session.add(vote)
    return render_template('vote.html',
                           lecturers=get_team_members(current_app.config['LECTURE_TEAM']),
                           form=form)


@web.route('/statistic/score/')
def score():
    res = db.session.query(User.name.label('name'),
                           func.avg(Vote.content).label('content'),
                           func.avg(Vote.gesture).label('gesture'),
                           func.avg(Vote.voice).label('voice')
                           ).join(Vote, Vote.lecturer == User.username
                                  ).filter_by(event_id=current_app.config['EVENT_ID']
                                              ).group_by(Vote.lecturer)
    res = sorted(res, key=lambda i: (i.content + i.gesture + i.voice), reverse=True)
    return render_template('score.html', res=res)


@web.route('/statistic/vote_status/')
def vote_status():
    lecturers = get_team_members(current_app.config['LECTURE_TEAM'])
    voters = []
    for voter in get_team_members(current_app.config['VOTE_TEAM']):
        votes = [i.lecturer for i in Vote.query.filter_by(
            voter=voter.username, event_id=current_app.config['EVENT_ID'])]
        voters.append(
            {"name": voter.name,
             "votes": [True if lecturer.username in votes else False for lecturer in lecturers]})
    return render_template('vote_status.html', lectures=lecturers, voters=voters)
