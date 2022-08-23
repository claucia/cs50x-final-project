from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, flash, url_for
from flask_login import login_required
from sqlalchemy import or_, and_
from app.models import BLOOD_BAG_EXPIRY_TIME_IN_DAYS, Role, Donor, Donation
from app.app import app
from app.forms import CreateDonorForm, EditDonorForm, CreateDonationForm, SearchDonorForm
from app.extensions import db
from app.utils import role_required


@app.route('/donors', methods=['GET'])
@login_required
@role_required(Role.ADMIN)
def list_donors():

    form = SearchDonorForm(request.args)
    donors = []

    filters = []
    name_criteria = form.name.data
    abo_rh_criteria = form.abo_rh.data

    if (name_criteria):
        name_filter = or_(
            Donor.first_name.ilike(f'%{name_criteria}%'),
            Donor.last_name.ilike(f'%{name_criteria}%')
        )
        filters.append(name_filter)

    if (abo_rh_criteria):
        abo_rh_filter = (Donor.abo_rh == abo_rh_criteria)
        filters.append(abo_rh_filter)

    donors = Donor.query.filter(and_(*filters))
    return render_template('donor/list_donor.html', donors=donors, form=form)


@app.route('/donors/new', methods=['POST', 'GET'])
@login_required
@role_required(Role.ADMIN)
def create_donor():

    form = CreateDonorForm(request.form)
    if request.method == 'POST' and form.validate():

        if Donor.query.filter_by(email=form.email.data).first():
            flash('This email/donor has already been registered', 'error')
            app.logger.info('%s has already been registered', form.email.data)
            return render_template('donor/create_donor.html', form=form)

        # Processo de instaciar uma classe
        # donor -> object of Donor
        # Donor(...) -> chama a construdor da class Donor para criar um objeto/instancia
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

    return render_template('donor/create_donor.html', form=form)


@app.route('/donors/edit/<int:donor_id>', methods=['POST', 'GET'])
@login_required
@role_required(Role.ADMIN)
def edit_donor(donor_id):

    donor = Donor.query.get(donor_id)
    if donor is None:
        flash('This donor could not be found', 'error')
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

    return render_template('donor/edit_donor.html', form=form)


@app.route('/donors/create-donation/<int:donor_id>', methods=['POST', 'GET'])
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
                            expiry_date=donation_date + timedelta(days=BLOOD_BAG_EXPIRY_TIME_IN_DAYS))

        donor.last_donation_date = donation_date

        db.session.add(donation)
        db.session.commit()

        flash('The donation has been registered')
        return redirect(url_for('list_donors'))

    form.first_name.data = donor.first_name
    form.last_name.data = donor.last_name
    form.abo_rh.data = donor.abo_rh
    form.last_donation_date.data = donor.last_donation_date

    return render_template('donor/create_donation.html', form=form)
