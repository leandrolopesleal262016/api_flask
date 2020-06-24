import os

SQLLITE = "app/static/telefones.db"
db = os.path.join(os.path.dirname(__file__), 'app\\static\\telefones.db')
SQLALCHEMY_DATABASE_URI = f"sqlite:///{db}"
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = False