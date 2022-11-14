"""
Sample API Module Package
"""
from flask import Blueprint

api_v1 = Blueprint('api_v1', __name__)


from . import calculator, info, admin, problem, user, hot_user, cold_user
