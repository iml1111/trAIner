from flask import g, jsonify, current_app
from flask_validation_extended import Json, Validator, Route
from app.api.response import response_200, bad_request, created
from app.api.decorator import timer
from model.mongodb import User, MasterConfig, Log
from flask import Blueprint
from flask_jwt_extended import (
    get_jwt_identity,
    create_refresh_token,
    create_access_token,
    jwt_required,
    set_access_cookies
)

api = Blueprint('auth', __name__)

@api.route('/sample', methods=['GET'])
@Validator(bad_request)
@timer
def sample_api():
    """sample API"""
    user = User(current_app.db).get_userinfo("16011090")
    return response_200(user)


@api.route('/signin', methods=['POST'])
@Validator(bad_request)
@timer
def sign_in(
    id=Json(str),
    pw=Json(str)
):
    """로그인"""
    user = User(current_app.db).get_password_with_id(id)
    if not user or user['password'] is None:
        return bad_request("Authentication failed.")
    if user['password'] != pw:
        return bad_request("Authentication failed.")

    user_oid = str(user['_id'])
    access_token = create_access_token(user_oid)

    resp = jsonify({'login': True})
    set_access_cookies(resp, access_token)
    return resp, 200
