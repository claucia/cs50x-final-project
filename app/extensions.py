from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Create instances of the main class of each extension
db = SQLAlchemy()

login = LoginManager()
login.login_view = 'login'
