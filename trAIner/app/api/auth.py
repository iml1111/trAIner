from flask import Blueprint
from model.mongodb import User
from app.api.decorator import timer
from flask import g, jsonify, current_app
from sejong_univ_auth import auth, DosejongSession
from flask_validation_extended import Json, Validator
from app.api.response import response_200, bad_request
from flask_jwt_extended import (
    get_jwt_identity,
    create_refresh_token,
    create_access_token,
    jwt_required,
    set_access_cookies,
    unset_jwt_cookies,
)

api = Blueprint('auth', __name__)


@api.route('auth-test')
@jwt_required()
def auth_test_api():
    """인증 테스트"""
    return response_200("hello, %s" % get_jwt_identity())


@api.route('/sign-in', methods=['POST'])
@Validator(bad_request)
@timer
def sign_in(
    id=Json(str),
    pw=Json(str),
    isPersist=Json(bool)
):
    """로그인"""
    user = User(current_app.db).get_password_with_id(id)
    if not user or user['password'] is None:
        return bad_request("Authentication failed.")
    if user['password'] != pw:
        return bad_request("Authentication failed.")

    user_oid = str(user['_id'])
    resp = jsonify(
        {   
            'msg': 'success',
            'refresh_token': create_refresh_token(user_oid)
        }
    )
    set_access_cookies(
        response=resp,
        encoded_access_token=create_access_token(user_oid),
        max_age=current_app.config['COOKIE_MAX_AGE'] if isPersist else 1
    )
    return resp


@api.route('/sign-up', methods=['POST'])
@Validator(bad_request)
@timer
def sign_up(
    id=Json(str),
    pw=Json(str)
):
    """회원가입"""
    user_model = User(current_app.db)
    if user_model.get_password_with_id(id):
        return bad_request('user already exists.')
    
    sejong_user = auth(id=id, password=pw, methods=DosejongSession)
    if not sejong_user.is_auth or sejong_user.is_auth is None:
        return bad_request('you are not sejong user.')

    user_oid = user_model.insert_user({
        'userId': id,
        'password': pw,
        'name': sejong_user.body['name'],
        'isHotUser': False
    }).inserted_id

    user_oid = str(user_oid)
    resp = jsonify(
        {
            'msg': 'created',
            'refresh_token': create_refresh_token(user_oid)
        }
    )
    set_access_cookies(
        response=resp,
        encoded_access_token=create_access_token(user_oid),
        max_age=1
    )
    return resp


@api.route('sign-out', methods=['POST'])
@Validator(bad_request)
@jwt_required()
@timer
def sign_out():
    """로그아웃"""
    resp = jsonify({})
    unset_jwt_cookies(resp)
    return resp


@api.route('/refresh')
@jwt_required(refresh=True)
def auth_token_refresh():
    """JWT Token Refresh"""
    user_oid = get_jwt_identity()
    resp = jsonify(
        {
            'msg': 'success',
            'refresh_token': create_refresh_token(user_oid)
        }
    )
    set_access_cookies(resp, create_access_token(user_oid))
    return resp