from flask import url_for, flash, render_template
from flask_login import current_user, login_user, logout_user
from werkzeug.utils import redirect

from app.forms.user import LoginForm
from app.models.user import User
from app.routes import bp_index


@bp_index.route('/', methods=['GET', 'POST'])
@bp_index.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@bp_index.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('index.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index.index'))
    return render_template('login.html', title='Sign In', form=form)


@bp_index.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
