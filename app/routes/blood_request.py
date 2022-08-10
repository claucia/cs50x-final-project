from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for
from app.app import app
from flask_login import login_required
from app.utils import role_required
from app.forms import CreateBloodRequestForm, SearchBloodRequestForm
from app.extensions import db
from app.models import Role, BloodRequest
from sqlalchemy import or_, and_


@app.route('/blood-requests', methods=['POST', 'GET'])
@login_required
@role_required(Role.ADMIN)
def list_blood_requests():

    form = SearchBloodRequestForm(request.form)
    requests = []

    if request.method == 'POST' and form.validate():

        filters = []
        name_criteria = form.name.data
        abo_rh_criteria = form.abo_rh.data

        if(name_criteria):
            name_filter = or_(
                BloodRequest.patient_first_name.ilike(f'%{name_criteria}%'),
                BloodRequest.patient_last_name.ilike(f'%{name_criteria}%')
            )
            filters.append(name_filter)

        if(abo_rh_criteria):
            abo_rh_filter = (BloodRequest.abo_rh == abo_rh_criteria)
            filters.append(abo_rh_filter)

        requests = BloodRequest.query.filter(and_(*filters))
        return render_template('blood_request/list.html', requests=requests, form=form)

    requests = BloodRequest.query.all()
    return render_template('blood_request/list.html', requests=requests, form=form)


@app.route('/blood-requests/new', methods=['POST', 'GET'])
@login_required
@role_required(Role.ADMIN)
def create_blood_request():

    form = CreateBloodRequestForm(request.form)
    if request.method == 'POST' and form.validate():

        request_date = datetime.now()
        blood_request = BloodRequest(patient_first_name=form.patient_first_name.data,
                                     patient_last_name=form.patient_last_name.data,
                                     abo_rh=form.abo_rh.data,
                                     units=form.units.data,
                                     request_date=request_date)

        db.session.add(blood_request)
        db.session.commit()

        flash('The blood request has been registered')
        app.logger.info('A blood request has been registered for %s %s',
                        form.patient_first_name.data, form.patient_last_name.data)
        return redirect(url_for('list_blood_requests'))

    return render_template('blood_request/create.html', form=form)
