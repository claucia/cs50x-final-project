from flask import Flask, render_template, request, redirect, flash, url_for
from flask_login import login_required
from app.models import Role, Donor
from app.app import app
from app.forms import CreateDonorForm
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
