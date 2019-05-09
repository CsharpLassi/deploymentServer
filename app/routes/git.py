import hmac
from flask import request, jsonify, current_app, render_template, redirect
from git import Repo

from app.forms import GitHookFormNew
from app.routes import git_webhook


@git_webhook.route('/git/hook/new', methods=['GET', 'POST'])
def new_git_hook():
    form = GitHookFormNew()
    if form.validate_on_submit():
        return redirect('/git/hook')
    return render_template('git/new.html', form=form)


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
