import hmac
from flask import request, jsonify, current_app, render_template, redirect, url_for
from git import Repo

from app import db
from app.forms import GitHookFormNew
from app.forms.gitHook import GitHookFormEdit
from app.models.gitHook import GitHook
from app.routes import git_webhook


@git_webhook.route('/git/hook/new', methods=['GET', 'POST'])
def new_git_hook():
    form = GitHookFormNew()
    if form.validate_on_submit():
        hook = GitHook(name=form.name.data, secret=form.secret.data)
        db.session.add(hook)
        db.session.commit()
    return render_template('git/new.html', form=form)


@git_webhook.route('/git/hook', methods=['GET'])
def list_git_hook():
    hooks = GitHook.query.all()
    return render_template('git/list.html', hooks=hooks)


@git_webhook.route('/git/hook/<int:id>', methods=['GET', 'POST'])
def edit_git_hook(id):
    hook = GitHook.query.get(id)
    form = GitHookFormEdit()
    if form.validate_on_submit():
        hook.name = form.name.data
        hook.secret = form.secret.data

        db.session.commit()

    form.name.data = hook.name
    form.secret.data = hook.secret

    return render_template('git/edit.html', form=form, hook=hook)


@git_webhook.route('/github/<int:id>', methods=['POST'])
def handle_github_hook(id):
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
