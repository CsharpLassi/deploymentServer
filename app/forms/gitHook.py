from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class GitHookFormNew(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    secret = StringField('Secret', validators=[DataRequired()])
    repo_path = StringField('Repo path', validators=[DataRequired()])
    submit = SubmitField('Register')


class GitHookFormEdit(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    secret = StringField('Secret', validators=[DataRequired()])
    repo_path = StringField('Repo path', validators=[DataRequired()])
    url = StringField('Hook url', render_kw={'readonly': True})
    submit = SubmitField('Save')
