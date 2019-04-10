from flask import Blueprint

auth = Blueprint('auth', __name__)

from project.users import views