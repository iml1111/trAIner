from model.mongodb import User
from flask import g, jsonify, current_app
from flask_validation_extended import Validator
from app.api.decorator import timer, login_required
from app.api.response import response_200, bad_request
from . import api_v1 as api


@api.route('/users/me', methods=['GET'])
@Validator(bad_request)
@login_required
@timer
def get_my_info():
    """내 정보 반환"""
    user = User(current_app.db).get_userinfo(
        user_oid=g.user_oid
    )
    return response_200(user)


