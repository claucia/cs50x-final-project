from flask import Flask, render_template, request, redirect, flash, url_for
from flask_login import current_user, login_required
from sqlalchemy import or_, and_
from werkzeug.security import generate_password_hash, check_password_hash
from app.app import app
from app.forms import ChangePasswordForm, CreateUserForm, EditUserForm, SearchUserForm
from app.models import Role, User
from app.extensions import db
from app.utils import role_required

# @ = decorator. It is used to associate a particular function with a particular URL
@app.route('/users', methods=['GET'])
@login_required
@role_required(Role.ADMIN)
def list_users():

    form = SearchUserForm(request.args)
    users = []

    filters = []
    name_criteria = form.name.data
    role_criteria = form.role.data
    
    if(name_criteria):
        name_filter = or_(
            # .ilike: string comparisons case insensitive
            User.first_name.ilike(f'%{name_criteria}%'),
            User.last_name.ilike(f'%{name_criteria}%')
        )
        filters.append(name_filter)

    if(role_criteria):
        role_filter = (User.role == role_criteria)
        filters.append(role_filter)

    # function filter(*criterion) means you can use tuple as it's argument
    users = User.query.filter(and_(*filters)).all()

    # 'users=users'
    # first users = name of a variable I want to give to the template-list_user.html
    # second users = this is theactual variable that I want to get the value from
    # The same aplies to form=form 
    return render_template('user/list_user.html', users=users, form=form)


@app.route('/users/new', methods=['POST', 'GET'])
@login_required
@role_required(Role.ADMIN)
def create_user():

    form = CreateUserForm(request.form)
    # handle the POST request
    if request.method == 'POST' and form.validate():

        if User.query.filter_by(email=form.email.data).first():
            flash('This email has already been registered', 'error')
            app.logger.info('%s has already been registered', user.email)
            return render_template('register.html', form=form)

        user = User(first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email.data,
                    password_hash=generate_password_hash(form.password.data),
                    role=form.role.data)

        db.session.add(user)
        db.session.commit()

        # flash = put message in HTTP session to be used in the template to be displayed to the end user 
        flash('The user has been registered')
        app.logger.info('%s has been registered', user.email)
        return redirect(url_for('list_users'))
    # otherwise handle the GET request
    return render_template('user/create_user.html', form=form)


# `<int:user_id>` Flask's bult-in URL converter
@app.route('/users/edit/<int:user_id>', methods=['POST', 'GET'])
@login_required
@role_required(Role.ADMIN)
def edit_user(user_id):

    # It get the user in the database with this id. This line will do the SELECT.
    # SELECT users.id AS users_id, users.first_name AS users_first_name, users.last_name AS users_last_name, users.email AS users_email, users.password_hash AS users_password_hash, users.role AS users_role FROM users WHERE users.id = ?
    user = User.query.get(user_id)

    if user is None:
        flash('This user could not be found', 'error')
        return redirect(url_for('list_users'))

    form = EditUserForm(request.form)
    if request.method == 'POST' and form.validate():

        # This block of code will copy values from the form to the object
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        
        # It will save everything in the dadabase
        db.session.commit()

        flash('The user has been updated')
        return redirect(url_for('list_users'))

    # This block of code will copy user's data (user.first_name) that got in the database to the form's fields (form.first_name.data)
    form = EditUserForm()
    form.first_name.data = user.first_name
    form.last_name.data = user.last_name
    form.email.data = user.email
    form.role.data = user.role

    return render_template('user/edit_user.html', form=form)


@app.route('/change-password', methods=['POST', 'GET'])
@login_required
def change_password():

    form = ChangePasswordForm(request.form)
    if request.method == 'POST' and form.validate():

        if check_password_hash(current_user.password_hash, form.current_password.data) == False:
            flash('Your current password is incorrect', 'error')
            return redirect(url_for('change_password'))

        user = User.query.get(current_user.id)
        user.password_hash = generate_password_hash(form.new_password.data)
        db.session.commit()

        flash('Your password has been updated')
        return redirect(url_for('home'))

    return render_template('user/change_password.html', form=form)
