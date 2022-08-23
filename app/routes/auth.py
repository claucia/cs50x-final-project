from flask import render_template, request, redirect, flash, url_for
from flask_login import current_user, login_user, logout_user
from werkzeug.security import check_password_hash
from app.app import app
from app.forms import LoginForm
from app.models import User


@app.route('/login', methods=['POST', 'GET'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():

        email = form.email.data
        user = User.query.filter_by(email=email).first()

        password = form.password.data
        if user is not None and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials', 'error')
            return redirect(url_for('login'))

    return render_template('auth/login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You\'ve been logged out')
    return redirect(url_for('login'))
