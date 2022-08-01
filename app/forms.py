from wtforms import Form, StringField, PasswordField, SelectField, SubmitField, validators
from app.models import BloodType, Role

user_role_choices = [(Role.ADMIN, 'Administrator'),
                     (Role.PHYSICIAN, 'Physician')]

blood_type_choices = [(BloodType.A_POSITIVE, BloodType.A_POSITIVE),
                      (BloodType.A_NEGATIVE, BloodType.A_NEGATIVE),
                      (BloodType.B_POSITIVE, BloodType.B_POSITIVE),
                      (BloodType.B_NEGATIVE, BloodType.B_NEGATIVE),
                      (BloodType.AB_POSITIVE, BloodType.AB_POSITIVE),
                      (BloodType.AB_NEGATIVE, BloodType.AB_NEGATIVE),
                      (BloodType.O_POSITIVE, BloodType.O_POSITIVE),
                      (BloodType.O_NEGATIVE, BloodType.O_NEGATIVE)]


class CreateUserForm(Form):
    first_name = StringField(
        'First name',
        [validators.DataRequired(), validators.Length(min=2, max=100)])
    last_name = StringField(
        'Last name',
        [validators.DataRequired(), validators.Length(min=2, max=100)])
    email = StringField(
        'E-mail',
        [validators.DataRequired(), validators.Length(min=6, max=100)])
    password = PasswordField(
        'Password',
        [validators.DataRequired()])
    role = SelectField(
        'Role',
        [validators.DataRequired()],
        choices=user_role_choices)
    submit = SubmitField('Create user')


class EditUserForm(Form):
    first_name = StringField(
        'First name',
        [validators.DataRequired(), validators.Length(min=2, max=100)])
    last_name = StringField(
        'Last name',
        [validators.DataRequired(), validators.Length(min=2, max=100)])
    email = StringField(
        'E-mail',
        [validators.DataRequired(), validators.Length(min=6, max=100)],
        render_kw={'readonly': True})
    role = SelectField(
        'Role',
        [validators.DataRequired()],
        choices=user_role_choices)
    submit = SubmitField('Update user')


class LoginForm(Form):
    email = StringField(
        'E-mail',
        [validators.DataRequired()])
    password = PasswordField(
        'Password',
        [validators.DataRequired()])
    submit = SubmitField('Login')


class ChangePasswordForm(Form):
    current_password = PasswordField(
        'Current password',
        [validators.DataRequired()])
    new_password = PasswordField(
        'New password',
        [validators.DataRequired()])
    submit = SubmitField('Change password')


# Donor
class CreateDonorForm(Form):
    first_name = StringField(
        'First name',
        [validators.DataRequired(), validators.Length(min=2, max=100)])
    last_name = StringField(
        'Last name',
        [validators.DataRequired(), validators.Length(min=2, max=100)])
    abo_rh = SelectField(
        u'ABO/Rh', choices=blood_type_choices)
    phone_number = StringField(
        'Phone number',
        [validators.DataRequired(), validators.Length(min=6, max=100)])
    email = StringField(
        'E-mail',
        [validators.DataRequired(), validators.Length(min=6, max=100)])
    submit = SubmitField('Create donor')
