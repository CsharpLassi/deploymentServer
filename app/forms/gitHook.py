from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class GitHookFormNew(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    secret = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')
