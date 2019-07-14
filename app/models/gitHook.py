from app import db


class GitHook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, index=True)
    secret = db.Column(db.Text)
    repo_path = db.Column(db.Text)
