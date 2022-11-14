"""
Admin Interface API
- CTR Model 기준 임계치 파라미터 조절

"""
from flask import abort
from flask_validation_extended import Validator, Query
from flask_validation_extended import ValidationRule
from app.api.response import response_200, bad_request
from app.api.decorator import timer
from app.api.v1 import api_v1 as api


