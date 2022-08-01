from flask import session
from werkzeug.security import generate_password_hash
from app.models import Role, User, Donor
from app.extensions import db
from app.app import app


def setup():
    create_tables()
    if should_populate_database() is True:
        invalidate_http_sessions()
        create_admin_user()
        create_physician_user()
        create_donor()


def create_tables():
    app.logger.info("Creating tables that do not exist...")
    db.create_all()


def should_populate_database():
    return User.query.first() is None


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


def create_donor():
    app.logger.info("Creating donor...")
    donor = Donor(first_name='Laila',
                  last_name='Doe',
                  abo_rh='AB+',
                  phone_number='083 000 0000',
                  email='laila@mail.com')
    db.session.add(donor)
    db.session.commit()