from flask import Flask, render_template, request, redirect, flash, url_for
from flask_login import current_user, login_required
from sqlalchemy import or_, and_
from werkzeug.security import generate_password_hash, check_password_hash
from app.app import app
from app.forms import ChangePasswordForm, CreateUserForm, EditUserForm, SearchUserForm
from app.models import Role, User
from app.extensions import db
from app.utils import role_required


@app.route('/users', methods=['POST', 'GET'])
@login_required
@role_required(Role.ADMIN)
def list_users():

    form = SearchUserForm(request.form)
    users = []

    if request.method == 'POST' and form.validate():

        filters = []
        name_criteria = form.name.data
        role_criteria = form.role.data
        print(f'Name: {name_criteria}')

        if(name_criteria):
            name_filter = or_(
                # .ilike: string comparisons case insensitive
                User.first_name.ilike(f'%{name_criteria}%'),
                User.last_name.ilike(f'%{name_criteria}%'),
            )
            filters.append(name_filter)

        if(role_criteria):
            role_filter = (User.role == role_criteria)
            filters.append(role_filter)

        # The function filter(*criterion) means you can use tuple as it's argument
        users = User.query.filter(and_(*filters))
        return render_template('user/list.html', users=users, form=form)

    users = User.query.all()
    return render_template('user/list.html', users=users, form=form)


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


    # Busca no banco de dados usuário com esse id
    # Esta linha fará o SELECT
    # SELECT users.id AS users_id, users.first_name AS users_first_name, users.last_name AS users_last_name, users.email AS users_email, users.password_hash AS users_password_hash, users.role AS users_role FROM users WHERE users.id = ?
    user = User.query.get(user_id)

    if user is None:
        flash('This user could not be found')
        return redirect(url_for('list_users'))

    form = EditUserForm(request.form)
    if request.method == 'POST' and form.validate():

        # Copiar valores do formulário para o objeto
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.role = form.role.data

        db.session.commit()

        flash('The user has been updated')
        return redirect(url_for('list_users'))

    # Copiar os dados do usuário (user.first_name) que buscou no banco de dados para os campos do formulário (form.first_name.data)                                                       
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

    return render_template('user/change_password.html', form=form)
