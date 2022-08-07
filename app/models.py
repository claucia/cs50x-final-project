from flask_login import UserMixin
from app.extensions import db
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


BLOOD_BAG_EXPIRY_TIME_IN_DAYS = 42


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


class BloodType(object):
    __slots__ = ()
    A_POSITIVE = 'A+'
    A_NEGATIVE = 'A-'
    AB_POSITIVE = 'AB+'
    AB_NEGATIVE = 'AB-'
    B_POSITIVE = 'B+'
    B_NEGATIVE = 'B-'
    O_POSITIVE = 'O+'
    O_NEGATIVE = 'O-'


class Donor(db.Model):
    __tablename__ = 'donors'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    abo_rh = db.Column(db.String(3), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    last_donation_date = db.Column(db.DateTime(), nullable=True)


class Donation(db.Model):
    __tablename__ = 'donations'

    id = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.Integer, db.ForeignKey(Donor.id))
    abo_rh = db.Column(db.String(3), nullable=False)
    donation_date = db.Column(db.DateTime(), nullable=False)
    expiry_date = db.Column(db.DateTime(), nullable=False)

    donor = relationship('Donor')
