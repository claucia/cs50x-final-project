from flask import render_template
from flask_login import login_required, current_user
from app.app import app
from app.models import Role
from app.utils import role_required


@app.route('/')
@login_required
def home():
    return render_template('home/home.html')
