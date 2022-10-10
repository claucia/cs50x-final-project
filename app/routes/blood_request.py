from datetime import datetime
from random import choices
from flask import Flask, render_template, request, redirect, flash, url_for
from app.app import app
from flask_login import login_required, current_user
from app.utils import role_required
from app.forms import CreateBloodRequestForm, FulfillBloodRequestForm, SearchBloodRequestForm
from app.extensions import db
from app.models import CAN_RECEIVE_BLOOD_FROM, BloodRequestStatus, Donation, Role, BloodRequest
from sqlalchemy import or_, and_, asc


@app.route('/blood-requests', methods=['GET'])
@login_required
def list_blood_requests():

    form = SearchBloodRequestForm(request.args)
    filters = []
    requests = []

    if(current_user.is_physician()):
        user_filter = (BloodRequest.user == current_user)
        filters.append(user_filter)

    name_criteria = form.name.data
    abo_rh_criteria = form.abo_rh.data
    status_criteria = form.status.data

    if (name_criteria):
        name_filter = or_(
            BloodRequest.patient_first_name.ilike(f'%{name_criteria}%'),
            BloodRequest.patient_last_name.ilike(f'%{name_criteria}%')
        )
        filters.append(name_filter)

    if (abo_rh_criteria):
        abo_rh_filter = (BloodRequest.abo_rh == abo_rh_criteria)
        filters.append(abo_rh_filter)

    if (status_criteria):
        status_filter = (BloodRequest.status == status_criteria)
        filters.append(status_filter)

    requests = BloodRequest.query.filter(and_(*filters)).all()
    return render_template('blood_request/list_blood_request.html', 
        requests=requests, 
        form=form,
        current_user=current_user)


@app.route('/blood-requests/new', methods=['POST', 'GET'])
@login_required
@role_required(Role.PHYSICIAN)
def create_blood_request():

    form = CreateBloodRequestForm(request.form)
    if request.method == 'POST' and form.validate():

        request_date = datetime.now()
        blood_request = BloodRequest(patient_first_name=form.patient_first_name.data,
                                     patient_last_name=form.patient_last_name.data,
                                     abo_rh=form.abo_rh.data,
                                     units=form.units.data,
                                     request_date=request_date,
                                     status=BloodRequestStatus.PENDING,
                                     user=current_user)

        db.session.add(blood_request)
        db.session.commit()

        flash('The blood request has been registered')
        # app.logger.info('A blood request has been registered for %s %s',
        #                 form.patient_first_name.data, form.patient_last_name.data)
        return redirect(url_for('list_blood_requests'))

    return render_template('blood_request/create_blood_request.html', form=form)


@app.route('/blood-requests/fulfill/<int:blood_request_id>', methods=['POST', 'GET'])
@login_required
@role_required(Role.ADMIN)
def fulfill_blood_request(blood_request_id):

    blood_request = BloodRequest.query.get(blood_request_id)
    if blood_request is None:
        flash('This blood request could not be found', 'error')
        return redirect(url_for('list_blood_requests'))

    # Obtain compatible blood types
    compatible_types = CAN_RECEIVE_BLOOD_FROM[blood_request.abo_rh]

    form = FulfillBloodRequestForm(request.form)
    if request.method == 'POST' and form.validate():

        # Approving?
        if (request.form.get("submit") == "Approve"): 

            # Can the status be changed?
            if (blood_request.status != BloodRequestStatus.PENDING):
                flash(f'This blood request cannot be approved', 'error')
                return redirect(request.url)

            # Obtain donation IDs selected by the user
            compatible_donation_ids = request.form.getlist('donation')

            # Validate the amount of donations selected by the user
            if (blood_request.units != len(compatible_donation_ids)):
                flash(f'You must select exactly {blood_request.units} donation(s) to fulfill this request', 'error')
                return redirect(request.url)

            # Find donations with the given donations IDs
            compatible_donations = Donation.query.filter(Donation.id.in_(compatible_donation_ids)).all()

            # Validate the amount of donations found in the database
            if (blood_request.units != len(compatible_donations)):
                flash(f'The seleted donation(s) cannot be used to fullfil this request. Please try again.', 'error')
                return redirect(request.url)

            # Iterate over each donation
            for donation in compatible_donations:

                # Validate blood type
                if (donation.abo_rh not in compatible_types):
                    flash(f'The seleted donation(s) cannot be used to fullfil this request. Please try again.', 'error')
                    return redirect(request.url)

                # Validate if it has not been associated with other blood request
                if (donation.blood_request_id is not None):
                    flash(f'The seleted donation(s) cannot be used to fullfil this request. Please try again.', 'error')
                    return redirect(request.url)

                # Associate each donation with the blood request
                donation.blood_request_id = blood_request_id

            # Update blood request status to approved
            blood_request.status = BloodRequestStatus.APPROVED

            # Persist changes to the database
            db.session.commit()

            flash('The blood request has been approved')
            return redirect(url_for('list_blood_requests'))

        # Rejecting?
        elif (request.form.get("submit") == "Reject"): 

            # Can the status be changed?
            if (blood_request.status != BloodRequestStatus.PENDING):
                flash(f'This blood request cannot be rejected', 'error')
                return redirect(request.url)

            # Update blood request status to rejected
            blood_request.status = BloodRequestStatus.REJECTED

            # Persist changes to the database
            db.session.commit()

            flash('The blood request has been rejected')
            return redirect(url_for('list_blood_requests'))

        # Hacking to do something else?
        else:

            flash('Unsupported action')
            return redirect(request.url)

    form = FulfillBloodRequestForm()
    form.patient_first_name.data = blood_request.patient_first_name
    form.patient_last_name.data = blood_request.patient_last_name
    form.abo_rh.data = blood_request.abo_rh
    form.units.data = blood_request.units
    form.status.data = blood_request.status

    ## Only allow approving or rejecting if the status of the request is Pending
    is_pending = (blood_request.status == BloodRequestStatus.PENDING)
    donations = []

    if (is_pending == True):

        # Find suitable donations that can be used for fulfilling the request
        donations = \
            Donation.query.filter(
                and_(
                    Donation.abo_rh.in_(compatible_types),
                    Donation.blood_request_id.is_(None),
                )
            ).all()

    else:

        # Find the donations that have been previously associated with this blood request
        donations = \
            Donation.query.filter(
                and_(
                    Donation.blood_request_id == blood_request_id,
                )
            ).all()

    is_rejected = (blood_request.status == BloodRequestStatus.REJECTED)

    return render_template('blood_request/fulfill_blood_request.html', 
        form=form,
        donations=donations,
        is_pending=is_pending,
        is_rejected=is_rejected)
