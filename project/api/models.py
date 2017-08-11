import datetime

from project import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=False, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.created_at = datetime.datetime.utcnow()


def query_to_dict(query, fields):
    data = {}
    for field in fields:
        try:
            data[field] = getattr(query, field)
        except AttributeError as e:
            raise AttributeError(f'{field} not in query!') from e

    return data
