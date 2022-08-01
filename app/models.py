from flask_login import UserMixin
from app.extensions import db


class Role(object):
    __slots__ = ()
    ADMIN = 'admin'
    PHYSICIAN = 'physician'


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(10), nullable=False)

    def is_admin(self):
        return self.role == Role.ADMIN

    def is_physician(self):
        return self.role == Role.PHYSICIAN


class Donor(db.Model):
    __tablename__ = 'donors'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    abo_rh = db.Column(db.String(3), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    last_donation_date = db.Column(db.DateTime(), nullable=True)

    