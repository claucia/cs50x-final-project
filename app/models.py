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


CAN_RECEIVE_BLOOD_FROM = {

    BloodType.A_POSITIVE: [
        BloodType.A_POSITIVE, 
        BloodType.A_NEGATIVE,
        BloodType.O_POSITIVE,
        BloodType.O_NEGATIVE
    ],

    BloodType.A_NEGATIVE: [
        BloodType.A_NEGATIVE,
        BloodType.O_NEGATIVE
    ],

    BloodType.AB_POSITIVE: [
        BloodType.A_POSITIVE,
        BloodType.A_NEGATIVE,
        BloodType.B_POSITIVE,
        BloodType.B_NEGATIVE,
        BloodType.AB_POSITIVE,
        BloodType.AB_NEGATIVE,
        BloodType.O_POSITIVE,
        BloodType.O_NEGATIVE
    ],

    BloodType.AB_NEGATIVE: [
        BloodType.A_NEGATIVE,
        BloodType.B_NEGATIVE,
        BloodType.AB_NEGATIVE,
        BloodType.O_NEGATIVE
    ],

    BloodType.B_POSITIVE: [
        BloodType.B_POSITIVE,
        BloodType.B_NEGATIVE,
        BloodType.O_POSITIVE,
        BloodType.O_NEGATIVE
    ],

    BloodType.B_NEGATIVE: [
        BloodType.B_NEGATIVE,
        BloodType.O_NEGATIVE
    ],

    BloodType.O_POSITIVE: [
        BloodType.O_POSITIVE,
        BloodType.O_NEGATIVE
    ],

    BloodType.O_NEGATIVE: [
        BloodType.O_NEGATIVE,
    ]

}

class BloodRequestStatus(object):
    __slots__ = ()
    PENDING = 'Pending'
    APPROVED = 'Approved'
    REJECTED = 'Rejected'


class Donor(db.Model):
    __tablename__ = 'donors'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    abo_rh = db.Column(db.String(3), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    last_donation_date = db.Column(db.Date(), nullable=True)


# Blood request
class BloodRequest(db.Model):
    __tablename__ = 'blood_requests'

    id = db.Column(db.Integer, primary_key=True)
    patient_first_name = db.Column(db.String(100), nullable=False)
    patient_last_name = db.Column(db.String(100), nullable=False)
    abo_rh = db.Column(db.String(3), nullable=False)
    units = db.Column(db.Integer, nullable=False)
    request_date = db.Column(db.DateTime(), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)

    user = relationship('User')


class Donation(db.Model):
    __tablename__ = 'donations'

    id = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.Integer, db.ForeignKey(Donor.id), nullable=False)
    blood_request_id = db.Column(
        db.Integer, db.ForeignKey(BloodRequest.id), nullable=True)
    abo_rh = db.Column(db.String(3), nullable=False)
    donation_date = db.Column(db.DateTime(), nullable=False)
    expiry_date = db.Column(db.DateTime(), nullable=False)

    donor = relationship('Donor')
    blood_request = relationship('BloodRequest')
