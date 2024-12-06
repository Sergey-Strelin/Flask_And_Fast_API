from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    date_of_birth = db.Column(db.DateTime, unique=False, nullable=False)
    agreement = db.Column(db.Boolean, unique=False, nullable=False)

    def __repr__(self):
        return f'User({self.name}, {self.email}, {self.date_of_birth.strftime("%d.%m.%Y")})'
