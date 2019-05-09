from flask import Blueprint

github_webhook = Blueprint('github_webhook', __name__, url_prefix='')

import app.routes.github
