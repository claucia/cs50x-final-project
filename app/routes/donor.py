from flask import Flask, render_template, request, redirect, flash, url_for
from flask_login import login_required
from app.models import Role, Donor
from app.app import app
from app.extensions import db
from app.utils import role_required

@app.route('/donors', methods=['POST', 'GET'])
@login_required
@role_required(Role.ADMIN)
def list_donors():
    donors = Donor.query.all()
    print(donors)
    return render_template('donor/list.html', donors=donors)