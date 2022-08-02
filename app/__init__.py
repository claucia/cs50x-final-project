from app import app
from app.models import User, Donor, BloodType
from app.routes import auth, home, user, donor
from app.utils import load_user
