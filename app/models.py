from datetime import datetime
from flask.ext.login import UserMixin

from app import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(128))
    balance = db.Column(db.Integer)

    def __repr__(self):
        return 'User #{} - {}'.format(self.id, self.username)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    to_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    amount = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    from_user = db.relationship('User', foreign_keys=[from_id], backref=db.backref('sent_transactions', uselist=True))
    to_user = db.relationship('User', foreign_keys=[to_id], backref=db.backref('received_transaction', uselist=True))