from flask import session
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
from app.models import BLOOD_BAG_EXPIRY_TIME_IN_DAYS, BloodType, Role, User, Donor, Donation
from app.extensions import db
from app.app import app


def setup():
    create_tables()
    if should_populate_database() is True:
        invalidate_http_sessions()
        populate_database()


def create_tables():
    app.logger.info("Creating tables that do not exist...")
    db.create_all()


def should_populate_database():
    return User.query.first() is None


def populate_database():
    create_admin_user()
    create_physician_user()
    create_a_positive_donor()
    create_a_negative_donor()


def invalidate_http_sessions():
    app.logger.info("Invalidating HTTP sessions...")
    session.clear()


def create_admin_user():
    app.logger.info("Creating admin user...")
    user = User(first_name='John',
                last_name='Doe',
                email='admin@mail.com',
                password_hash=generate_password_hash('123'),
                role=Role.ADMIN)
    db.session.add(user)
    db.session.commit()


def create_physician_user():
    app.logger.info("Creating physician user...")
    user = User(first_name='Jane',
                last_name='Doe',
                email='physician@mail.com',
                password_hash=generate_password_hash('123'),
                role=Role.PHYSICIAN)
    db.session.add(user)
    db.session.commit()


def create_a_positive_donor():
    app.logger.info("Creating A+ donor...")
    donor = Donor(first_name='Saara',
                  last_name='Mackie',
                  abo_rh=BloodType.A_POSITIVE,
                  phone_number='083 000 0000',
                  email='sm@mail.com')
    db.session.add(donor)
    create_donation(donor, donation_date=datetime_from_string(
        '2021-06-01 12:30:00'))
    create_donation(donor)
    db.session.commit()


def create_a_negative_donor():
    app.logger.info("Creating A- donor...")
    donor = Donor(first_name='Wayne',
                  last_name='Warner',
                  abo_rh=BloodType.A_NEGATIVE,
                  phone_number='083 000 0000',
                  email='ww@mail.com')
    db.session.add(donor)
    create_donation(donor)
    db.session.commit()


def create_donation(donor, donation_date=datetime.now()):
    app.logger.info(f"Creating {donor.abo_rh} donation...")
    donation = Donation(donor=donor,
                        abo_rh=donor.abo_rh,
                        donation_date=donation_date,
                        expiry_date=donation_date + timedelta(days=BLOOD_BAG_EXPIRY_TIME_IN_DAYS))
    db.session.add(donation)
    donor.last_donation_date = donation_date


def datetime_from_string(datetime_as_string):
    return datetime.strptime(datetime_as_string, '%Y-%m-%d %H:%M:%S')
