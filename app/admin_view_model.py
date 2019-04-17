from flask import url_for, request, redirect
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class BaseModelView(ModelView):
    def is_accessible(self):
        return current_user.username == 'Admin'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('web.login', next=request.url))


class UserModelView(BaseModelView):
    column_list = ('create_time', 'username', 'name', 'team_id')
    form_columns = ('name', 'team_id')
    can_create = False
    column_labels = {
        'create_time': '注册时间',
        'username': '用户名',
        'name': '姓名',
        'team_id': '组号'
    }
    column_display_pk = True


class VoteEventModelView(BaseModelView):
    can_delete = False
    column_list = ('create_time', 'event_id', 'lecture_team', 'vote_team', 'is_active')
    form_columns = ('lecture_team', 'vote_team', 'is_active')
    column_labels = {
        'event_id': '事件号',
        'create_time': '创建时间',
        'lecture_team': '演讲组号',
        'vote_team': '点评组号',
        'is_active': '是否为当前投票'
    }
    column_display_pk = True
