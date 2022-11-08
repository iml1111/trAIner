from flask import g, jsonify, current_app
from flask_validation_extended import Json, Validator
from app.api.response import response_200, bad_request, created
from app.api.decorator import timer
from model.mongodb import MasterConfig, Log
from flask import Blueprint

api = Blueprint('auth', __name__)


@api.route('/sign-in')
@timer
def sign_in():


    
    return response_200(list(Log().get_log(0, 10)))