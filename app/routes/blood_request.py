from flask import Flask, render_template, request, redirect, flash, url_for
from app.app import app
from flask_login import login_required
from app.forms import CreateBloodRequestForm
from app.extensions import db
from app.models import BloodRequest


@app.route('/create-blood-request', methods=['POST', 'GET'])
@login_required
def create_blood_request():

    form = CreateBloodRequestForm(request.form)
    if request.method == 'POST' and form.validate():

        blood_request = BloodRequest(patient_first_name=form.patient_first_name.data,
                                     patient_last_name=form.patient_last_name.data,
                                     abo_rh=form.abo_rh.data,
                                     how_many_units=form.how_many_units.data)

        db.session.add(blood_request)
        db.session.commit()

        flash('The blood request has been registered')
        app.logger.info('A blood request has been registered for %s %s',
                        form.patient_first_name.data, form.patient_last_name.data)
        return redirect(url_for('create_blood_request'))

    return render_template('blood_request/create.html', form=form)
