from flask import session
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
from app.models import BLOOD_BAG_EXPIRY_TIME_IN_DAYS, BloodRequest, BloodType, Role, User, Donor, Donation
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

    create_admin_user_1()
    create_admin_user_2()

    create_physician_user_1()
    create_physician_user_2()

    create_a_positive_donor()
    create_a_negative_donor()
    create_b_positive_donor()
    create_b_negative_donor()
    create_ab_positive_donor()
    create_ab_negative_donor()
    create_o_positive_donor()
    create_o_negative_donor()


def invalidate_http_sessions():
    app.logger.info("Invalidating HTTP sessions...")
    session.clear()


def create_admin_user_1():
    app.logger.info("Creating admin user...")
    user = User(first_name='John',
                last_name='Doe',
                email='admin1@mail.com',
                password_hash=generate_password_hash('123'),
                role=Role.ADMIN)
    db.session.add(user)
    db.session.commit()


def create_admin_user_2():
    app.logger.info("Creating admin user...")
    user = User(first_name='Deon',
                last_name='Forbes',
                email='admin2@mail.com',
                password_hash=generate_password_hash('123'),
                role=Role.ADMIN)
    db.session.add(user)
    db.session.commit()


def create_physician_user_1():
    app.logger.info("Creating physician user...")
    user = User(first_name='Jane',
                last_name='Doe',
                email='physician1@mail.com',
                password_hash=generate_password_hash('123'),
                role=Role.PHYSICIAN)
    db.session.add(user)
    create_blood_request(user, 'Melissa', 'Pemberton', BloodType.A_POSITIVE, 1)
    create_blood_request(user, 'Chaim', 'Castro', BloodType.B_NEGATIVE, 3)
    create_blood_request(user, 'Jaeden', 'Prosser', BloodType.AB_POSITIVE, 2)
    db.session.commit()


def create_physician_user_2():
    app.logger.info("Creating physician user...")
    user = User(first_name='Rianna',
                last_name='Gutierrez',
                email='physician2@mail.com',
                password_hash=generate_password_hash('123'),
                role=Role.PHYSICIAN)
    db.session.add(user)
    create_blood_request(user, 'Umer', 'Swift', BloodType.O_POSITIVE, 4)
    create_blood_request(user, 'Faris', 'Gillespie', BloodType.AB_NEGATIVE, 3)
    create_blood_request(user, 'Dexter', 'Forbes', BloodType.B_POSITIVE, 1)
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


def create_b_positive_donor():
    app.logger.info("Creating B+ donor...")
    donor = Donor(first_name='Matilda',
                  last_name='Stewart',
                  abo_rh=BloodType.B_POSITIVE,
                  phone_number='083 000 0000',
                  email='ms@mail.com')
    db.session.add(donor)
    create_donation(donor, donation_date=datetime_from_string(
        '2022-01-22 09:30:00'))
    create_donation(donor)
    db.session.commit()


def create_b_negative_donor():
    app.logger.info("Creating B- donor...")
    donor = Donor(first_name='Alishia',
                  last_name='Chan',
                  abo_rh=BloodType.B_NEGATIVE,
                  phone_number='083 000 0000',
                  email='ac@mail.com')
    db.session.add(donor)
    create_donation(donor, donation_date=datetime_from_string(
        '2020-12-25 11:30:00'))
    create_donation(donor)
    db.session.commit()


def create_ab_positive_donor():
    app.logger.info("Creating AB+ donor...")
    donor = Donor(first_name='Everett',
                  last_name='Gill',
                  abo_rh=BloodType.AB_POSITIVE,
                  phone_number='083 000 0000',
                  email='eg@mail.com')
    db.session.add(donor)
    create_donation(donor, donation_date=datetime_from_string(
        '2019-08-25 11:38:00'))
    create_donation(donor)
    db.session.commit()


def create_ab_negative_donor():
    app.logger.info("Creating AB- donor...")
    donor = Donor(first_name='Sky',
                  last_name='West',
                  abo_rh=BloodType.AB_NEGATIVE,
                  phone_number='083 000 0000',
                  email='sw@mail.com')
    db.session.add(donor)
    create_donation(donor, donation_date=datetime_from_string(
        '2020-03-16 11:55:00'))
    create_donation(donor)
    db.session.commit()


def create_o_positive_donor():
    app.logger.info("Creating O+ donor...")
    donor = Donor(first_name='Rui',
                  last_name='Flower',
                  abo_rh=BloodType.O_POSITIVE,
                  phone_number='083 000 0000',
                  email='rf@mail.com')
    db.session.add(donor)
    create_donation(donor, donation_date=datetime_from_string(
        '2020-03-16 11:55:00'))
    create_donation(donor)
    db.session.commit()


def create_o_negative_donor():
    app.logger.info("Creating O- donor...")
    donor = Donor(first_name='Hope',
                  last_name='Hook',
                  abo_rh=BloodType.O_NEGATIVE,
                  phone_number='083 000 0000',
                  email='hh@mail.com')
    db.session.add(donor)
    create_donation(donor, donation_date=datetime_from_string(
        '2020-03-16 11:55:00'))
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


def create_blood_request(user, patient_first_name, patient_last_name, abo_rh, units, request_date=datetime.now()):
    app.logger.info(f"Creating blood request...")
    request = BloodRequest(patient_first_name=patient_first_name,
                           patient_last_name=patient_last_name,
                           abo_rh=abo_rh,
                           units=units,
                           request_date=request_date,
                           user=user)

    db.session.add(request)


def datetime_from_string(datetime_as_string):
    return datetime.strptime(datetime_as_string, '%Y-%m-%d %H:%M:%S')
