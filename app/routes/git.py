import hmac
from flask import request, jsonify, current_app, render_template, redirect, url_for
from flask_login import login_required
from git import Repo

from app import db
from app.forms import GitHookFormNew
from app.forms.gitHook import GitHookFormEdit
from app.models.gitHook import GitHook
from app.routes import bp_git


@bp_git.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    form = GitHookFormNew()
    if form.validate_on_submit():
        hook = GitHook(name=form.name.data, secret=form.secret.data, repo_path=form.repo_path.data)
        db.session.add(hook)
        db.session.commit()
        return redirect(url_for('git.edit', hook_id=hook.id))
    return render_template('git/new.html', form=form)


@bp_git.route('/', methods=['GET'])
@bp_git.route('/index', methods=['GET'])
@login_required
def list():
    hooks = GitHook.query.all()
    return render_template('git/list.html', hooks=hooks)


@bp_git.route('/git/<hook_id>', methods=['GET', 'POST'])
@login_required
def edit(hook_id: int):
    hook = GitHook.query.get(hook_id)
    form = GitHookFormEdit()
    if form.validate_on_submit():
        hook.name = form.name.data
        hook.secret = form.secret.data
        hook.repo_path = form.repo_path.data
        db.session.commit()

    form.name.data = hook.name
    form.secret.data = hook.secret
    form.repo_path.data = hook.repo_path
    form.url.data = url_for('git.handle_github_hook', hook_id=hook.id, _external=True)
    return render_template('git/edit.html', form=form, hook=hook)


@bp_git.route('/hook/<hook_id>', methods=['POST'])
def handle_github_hook(hook_id):
    hook = GitHook.query.get(hook_id)
    update_repo = False

    signature = request.headers.get('X-Hub-Signature')

    if signature:
        sha, signature = signature.split('=')

        secret = str.encode(hook.secret)

        hashhex = hmac.new(secret, request.data, digestmod='sha1').hexdigest()
        if hmac.compare_digest(hashhex, signature):
            update_repo = True
    else:
        secret = request.json.get('secrete')

        update_repo = secret is not None and secret == hook.secret

    if update_repo:
        repo = Repo(hook.repo_path)
        origin = repo.remotes.origin
        origin.pull('--rebase')

        commit = request.json.get('after')
        if commit is not None:
            commit = commit[0:6]
            print('Repository updated with commit {}'.format(commit))
    return jsonify({}), 200
