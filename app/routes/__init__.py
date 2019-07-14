from flask import Blueprint

git_webhook = Blueprint('git', __name__, url_prefix='/git')

import app.routes.git
