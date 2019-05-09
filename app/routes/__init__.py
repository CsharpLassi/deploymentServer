from flask import Blueprint

git_webhook = Blueprint('git_webhook', __name__, url_prefix='')

import app.routes.git
