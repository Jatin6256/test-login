from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class users(db.Model):

    username = db.Column('username', db.String(100), primary_key = True)
    password = db.Column(db.String)


    def __init__(self, username, password):
        self.username = username
        self.password = password