"""
API Main Decorator
"""
import json
from functools import wraps
from time import time
from flask import current_app, g, Response
from controller import log
from config import config
from bson import ObjectId
from app.api.response import bad_access_token
from bson.errors import InvalidId
from model.mongodb import User
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity


def timer(func):
    """API Timer"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        process_time = time()
        result = func(*args, **kwargs)
        g.process_time = time() - process_time

        if current_app.config['DEBUG']:
            if config.TIMER_OUTPUT == 'response':
                if isinstance(result, Response):
                    data = json.loads(result.get_data())
                    data['process_time'] = g.process_time
                    result.set_data(json.dumps(data))
                elif isinstance(result, tuple):
                    result[0]['process_time'] = g.process_time
                else:
                    result['process_time'] = g.process_time
            elif config.TIMER_OUTPUT == 'log':
                log.info(f"process_time: {g.process_time}")

        return result
    return wrapper


def login_required(func):
    """유저 토큰 검증 데코레이터"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        try:
            user_oid = ObjectId(get_jwt_identity())
        except InvalidId:
            return bad_access_token
        g.user_oid = user_oid
        return func(*args, **kwargs)
    return wrapper