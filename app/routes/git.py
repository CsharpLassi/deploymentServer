import hmac
from flask import request, jsonify, current_app, render_template
from git import Repo

from app.routes import git_webhook


@git_webhook.route('/git/hook/new', methods=['GET'])
def new_git_hook():
    return render_template('index.html')


@git_webhook.route('/github', methods=['POST'])
def handle_github_hook():
    """ Entry point for github webhook """
    signature = request.headers.get('X-Hub-Signature')
    sha, signature = signature.split('=')

    secret = str.encode(current_app.config.get('GITHUB_SECRET'))

    hashhex = hmac.new(secret, request.data, digestmod='sha1').hexdigest()
    if hmac.compare_digest(hashhex, signature):
        repo = Repo(current_app.config.get('REPO_PATH'))
        origin = repo.remotes.origin
        origin.pull('--rebase')

        commit = request.json.get('after')
        if commit is not None:
            commit = commit[0:6]
            print('Repository updated with commit {}'.format(commit))
    return jsonify({}), 200
