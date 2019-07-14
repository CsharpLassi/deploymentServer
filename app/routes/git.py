import hmac
from flask import request, jsonify, current_app, render_template, redirect, url_for
from git import Repo

from app import db
from app.forms import GitHookFormNew
from app.forms.gitHook import GitHookFormEdit
from app.models.gitHook import GitHook
from app.routes import git_webhook


@git_webhook.route('/new', methods=['GET', 'POST'])
def new():
    form = GitHookFormNew()
    if form.validate_on_submit():
        hook = GitHook(name=form.name.data, secret=form.secret.data, repo_path=form.repo_path.data)
        db.session.add(hook)
        db.session.commit()
        return redirect(url_for('git.edit', id=hook.id))
    return render_template('git/new.html', form=form)


@git_webhook.route('/', methods=['GET'])
@git_webhook.route('/index', methods=['GET'])
def list():
    hooks = GitHook.query.all()
    return render_template('git/list.html', hooks=hooks)


@git_webhook.route('/git/<int:id>', methods=['GET', 'POST'])
def edit(id):
    hook = GitHook.query.get(id)
    form = GitHookFormEdit()
    if form.validate_on_submit():
        hook.name = form.name.data
        hook.secret = form.secret.data
        hook.repo_path = form.repo_path.data
        db.session.commit()

    form.name.data = hook.name
    form.secret.data = hook.secret
    form.repo_path.data = hook.repo_path
    form.url.data = url_for('git.handle_github_hook', id=hook.id, _external=True)
    return render_template('git/edit.html', form=form, hook=hook)


@git_webhook.route('/hook/<int:id>', methods=['POST'])
def handle_github_hook(id):
    """ Entry point for github webhook """
    signature = request.headers.get('X-Hub-Signature')
    sha, signature = signature.split('=')

    hook = GitHook.query.get(id)

    secret = str.encode(hook.secret)

    hashhex = hmac.new(secret, request.data, digestmod='sha1').hexdigest()
    if hmac.compare_digest(hashhex, signature):
        repo = Repo(hook.repo_path)
        origin = repo.remotes.origin
        origin.pull('--rebase')

        commit = request.json.get('after')
        if commit is not None:
            commit = commit[0:6]
            print('Repository updated with commit {}'.format(commit))
    return jsonify({}), 200
