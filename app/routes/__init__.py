from flask import Blueprint

bp_git = Blueprint('git', __name__, url_prefix='/git')
bp_index = Blueprint('index', __name__)

import app.routes.git
import app.routes.index
