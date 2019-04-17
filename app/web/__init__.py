from flask.blueprints import Blueprint

web = Blueprint('web', __name__, template_folder='templates', static_folder='static')

from . import index
from . import account
from . import errors
from . import function
