from flask import Flask, render_template, request, redirect, flash, url_for
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.app import app
from app.forms import ChangePasswordForm, CreateUserForm, EditUserForm
from app.models import Role, User
from app.extensions import db
from app.utils import role_required


@app.route('/users', methods=['POST', 'GET'])
@login_required
@role_required(Role.ADMIN)
def list_users():
    users = User.query.all()
    return render_template('user/list.html', users=users)


@app.route('/users/new', methods=['POST', 'GET'])
@login_required
@role_required(Role.ADMIN)
def create_user():

    form = CreateUserForm(request.form)
    if request.method == 'POST' and form.validate():

        if User.query.filter_by(email=form.email.data).first():
            flash('This email has already been registered')
            app.logger.info('%s has already been registered', user.email)
            return render_template('register.html', form=form)

        user = User(first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email.data,
                    password_hash=generate_password_hash(form.password.data),
                    role=form.role.data)

        db.session.add(user)
        db.session.commit()

        flash('The user has been registered')
        app.logger.info('%s has been registered', user.email)
        return redirect(url_for('list_users'))

    return render_template('user/create.html', form=form)


@app.route('/users/<int:user_id>', methods=['POST', 'GET'])
@login_required
@role_required(Role.ADMIN)
def edit_user(user_id):

    user = User.query.get(user_id)
    if user is None:
        flash('This user could not be found')
        return redirect(url_for('list_users'))

    form = EditUserForm(request.form)
    if request.method == 'POST' and form.validate():

        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.role = form.role.data

        db.session.commit()

        flash('The user has been updated')
        return redirect(url_for('list_users'))

    form = EditUserForm()
    form.first_name.data = user.first_name
    form.last_name.data = user.last_name
    form.email.data = user.email
    form.role.data = user.role

    return render_template('user/edit.html', form=form)


@app.route('/change-password', methods=['POST', 'GET'])
@login_required
def change_password():

    form = ChangePasswordForm(request.form)
    if request.method == 'POST' and form.validate():

        if check_password_hash(current_user.password_hash, form.current_password.data) == False:
            flash('Your current password is incorrect')
            return redirect(url_for('change_password'))

        user = User.query.get(current_user.id)
        user.password_hash = generate_password_hash(form.new_password.data)
        db.session.commit()

        flash('Your password has been updated')
        return redirect(url_for('home'))

    return render_template('user/change-password.html', form=form)
