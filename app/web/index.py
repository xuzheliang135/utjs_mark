from flask import redirect, url_for

from . import web


@web.route('/')
def index():
    return redirect(url_for('web.score'))
    # return render_template('index.html')



