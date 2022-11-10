from flask import g, jsonify, current_app
from flask_validation_extended import Json, Validator, Route
from app.api.response import response_200, bad_request, created
from app.api.decorator import timer
from model.mongodb import User, MasterConfig, Log
from flask import Blueprint
from sejong_univ_auth import auth
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


@api.route('/sign-in', methods=['POST'])
@Validator(bad_request)
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
    resp = jsonify(
        response_200({
            'refresh_token': create_refresh_token(user_oid)
        })
    )
    set_access_cookies(resp, create_access_token(user_oid))
    return resp, 200


@api.route('/sign-up', methods=['POST'])
@Validator(bad_request)
def sign_up(
    id=Json(str),
    pw=Json(str)
):
    """회원가입"""
    user_model = User(current_app.db)
    if user_model.get_password_with_id(id):
        return bad_request('user already exists.')
    
    sejong_user = auth(id=id, password=pw)
    if not sejong_user.is_auth or sejong_user.is_auth is None:
        return bad_request('you are not sejong user.')

    user_oid = user_model.insert_user({
        'id': id,
        'password': pw,
    }).inserted_id

    user_oid = str(user_oid)
    resp = jsonify(
        response_200({
            'refresh_token': create_refresh_token(user_oid)
        })
    )
    set_access_cookies(resp, create_access_token(user_oid))
    return resp, 200


@api.route('/refresh')
@jwt_required(refresh=True)
def auth_token_refresh():
    """JWT Token Refresh"""
    user_oid = get_jwt_identity()
    resp = jsonify(
        response_200({
            'refresh_token': create_refresh_token(user_oid)
        })
    )
    set_access_cookies(resp, create_access_token(user_oid))
    return resp, 200


@api.route('auth-test')
@jwt_required()
def auth_test_api():
    """인증 테스트"""
    return response_200("hello, %s" % get_jwt_identity())