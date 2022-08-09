from flask import Flask, render_template, request, redirect, flash, url_for
from app.app import app
from flask_login import login_required
from app.forms import BloodRequest


@app.route('/blood_request', methods=['POST', 'GET'])
@login_required
def blood_request():
    form = BloodRequest(request.form)
    return render_template('blood_request/blood_request.html', form=form)
