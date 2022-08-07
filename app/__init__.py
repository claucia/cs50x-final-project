from app import app
from app.models import Role, User, BloodType, Donor, Donation
from app.routes import auth, home, user, donor
from app.utils import load_user
