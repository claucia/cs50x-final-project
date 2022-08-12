from flask import render_template
from flask_login import login_required, current_user
from app.app import app
from app.models import BloodRequest, BloodRequestStatus, Donation, Role
from app.utils import role_required
from app.extensions import db
from sqlalchemy import func


@app.route('/')
@login_required
def home():

    blood_types_and_amounts = db.session.query(Donation.abo_rh, func.count(
        Donation.abo_rh)).group_by(Donation.abo_rh).all()

    blood_request_status_and_amounts = db.session.query(BloodRequest.status, func.count(
        BloodRequest.status)).group_by(BloodRequest.status).all()

    return render_template('home/home.html', blood_types_and_amounts=dict(blood_types_and_amounts), blood_request_status_and_amounts=dict(blood_request_status_and_amounts))
