"""Response Shortcuts"""
import json
from flask import Response

def response_200(result=None):
    if result is None:
        return {'msg': 'success'}, 200
    else:
        return {'msg': 'success', 'result': result}, 200

created = ({"msg": "created"}, 201)

no_content = ({}, 204)


def bad_request(description):
    return {'msg': 'fail', 'description': description}, 400


bad_access_token = (
    {
        'msg':'fail',
        'description': "Bad access token"
    }, 401
)

def forbidden(description):
    return {
        'msg': 'fail',
        'description': description
    }, 403


not_found = {
    'msg': 'fail',
    'description': "Resource not found."
}, 404


def make_resp(data: dict, status: int):
    """flask Response 객체 생성"""
    return Response(
        json.dumps(data),
        mimetype='application/json',
        status=status
    )