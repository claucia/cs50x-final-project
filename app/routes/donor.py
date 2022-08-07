from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, flash, url_for
from flask_login import login_required
from app.models import Role, Donor, Donation
from app.app import app
from app.forms import CreateDonorForm, EditDonorForm, CreateDonationForm
from app.extensions import db
from app.utils import role_required


@app.route('/donors', methods=['POST', 'GET'])
@login_required
@role_required(Role.ADMIN)
def list_donors():
    donors = Donor.query.all()
    return render_template('donor/list.html', donors=donors)


@app.route('/donors/new', methods=['POST', 'GET'])
@login_required
@role_required(Role.ADMIN)
def create_donor():

    form = CreateDonorForm(request.form)
    if request.method == 'POST' and form.validate():

        if Donor.query.filter_by(email=form.email.data).first():
            flash('This email/donor has already been registered')
            app.logger.info('%s has already been registered', form.email.data)
            return render_template('donor/create.html', form=form)

        donor = Donor(first_name=form.first_name.data,
                      last_name=form.last_name.data,
                      abo_rh=form.abo_rh.data,
                      phone_number=form.phone_number.data,
                      email=form.email.data)

        db.session.add(donor)
        db.session.commit()

        flash('The donor has been registered')
        app.logger.info('%s has been registered', donor.email)
        return redirect(url_for('list_donors'))

    return render_template('donor/create.html', form=form)


@app.route('/donors/<int:donor_id>', methods=['POST', 'GET'])
@login_required
@role_required(Role.ADMIN)
def edit_donor(donor_id):

    donor = Donor.query.get(donor_id)
    if donor is None:
        flash('This donor could not be found')
        return redirect(url_for('list_donors'))

    form = EditDonorForm(request.form)
    if request.method == 'POST' and form.validate():

        donor.first_name = form.first_name.data
        donor.last_name = form.last_name.data
        donor.phone_number = form.phone_number.data
        donor.email = form.email.data

        db.session.commit()

        flash('The donor has been updated')
        return redirect(url_for('list_donors'))

    form = EditDonorForm()
    form.first_name.data = donor.first_name
    form.last_name.data = donor.last_name
    form.abo_rh.data = donor.abo_rh
    form.phone_number.data = donor.phone_number
    form.email.data = donor.email

    return render_template('donor/edit.html', form=form)


@app.route('/donors/<int:donor_id>/create-donation', methods=['POST', 'GET'])
@login_required
@role_required(Role.ADMIN)
def create_donation(donor_id):
    donor = Donor.query.get(donor_id)

    form = CreateDonationForm(request.form)
    if request.method == 'POST' and form.validate():

        donation_date = datetime.now()
        donation = Donation(donor=donor,
                            abo_rh=donor.abo_rh,
                            donation_date=donation_date,
                            expiry_date=donation_date + timedelta(days=42))

        donor.last_donation_date = donation_date

        db.session.add(donation)
        db.session.commit()

        flash('The donation has been registered')
        return redirect(url_for('list_donors'))

    form.first_name.data = donor.first_name
    form.last_name.data = donor.last_name
    form.abo_rh.data = donor.abo_rh

    return render_template('donor/create-donation.html', form=form)
