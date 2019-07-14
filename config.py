import os

basedir = os.getcwd()


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    GITHUB_SECRET = os.environ.get('GITHUB_SECRET')
    REPO_PATH = os.environ.get('REPO_PATH')
