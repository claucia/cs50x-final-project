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

    blood_types_and_amounts = \
        db.session.query(
            Donation.abo_rh, 
            func.count(Donation.abo_rh)
        ).filter(
            Donation.blood_request_id.is_(None)
        ).group_by(
            Donation.abo_rh
        ).all()

    blood_stock = {}
    for item in blood_types_and_amounts:
        abo_rh = item[0]
        amount = item[1]
        blood_stock[abo_rh] = {
            'amount': amount,
            'level': calculate_level(amount) 
        }
    
    blood_request_status_and_amounts = \
        db.session.query(
            BloodRequest.status, 
            func.count(BloodRequest.status)
        ).group_by(
            BloodRequest.status
        ).all()

    return render_template('home/home.html', 
        blood_stock=blood_stock, 
        blood_request_status_and_amounts=dict(blood_request_status_and_amounts))


def calculate_level(amount):
    if (amount >= 10):
        return 'high'
    if (amount >= 5):
        return 'medium'
    if (amount >= 1):
        return 'low'
    return 'zero'
