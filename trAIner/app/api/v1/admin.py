"""
Admin Interface API
- CTR Model 기준 임계치 파라미터 조절 (default 3)
- Deep Model 기준 임계치 파라미터 조절 (default 1)
- Hot User Recom Score 랜덤 가중치 조절 (default 0.5)
- Topic Model 유사도 가중치 조절 (default 1)
"""
from flask_validation_extended import Validator, Query
from app.api.response import response_200, bad_request
from app.api.decorator import timer
from model.mongodb.master_config import MasterConfig
from app.api.v1 import api_v1 as api


@api.get('/admin/ctr-threshold')
@Validator(bad_request)
@timer
def get_ctr_threshold_api():
    """CTR Model 기준 임계치 파라미터 조절"""
    ctr_threshold = MasterConfig().get_config('ctr_threshold')
    ctr_threshold = ctr_threshold['value'] if ctr_threshold else 3
    return response_200(ctr_threshold or 3)


@api.put('/admin/ctr-threshold')
@Validator(bad_request)
@timer
def put_ctr_threshold_api(
    value=Query([float, int])
):
    """CTR Model 기준 임계치 파라미터 조절"""
    MasterConfig().set_config('ctr_threshold', value)
    return response_200()


@api.get('/admin/deep-threshold')
@Validator(bad_request)
@timer
def get_deep_threshold_api():
    """Deep Model 기준 임계치 파라미터 조절"""
    deep_threshold = MasterConfig().get_config('deep_threshold')
    deep_threshold = deep_threshold['value'] if deep_threshold else 1
    return response_200(deep_threshold or 1)


@api.put('/admin/deep-threshold')
@Validator(bad_request)
@timer
def put_deep_threshold_api(
    value=Query([float, int])
):
    """Deep Model 기준 임계치 파라미터 조절"""
    MasterConfig().set_config('deep_threshold', value)
    return response_200()


@api.get('/admin/hotuser-random')
@Validator(bad_request)
@timer
def get_hotuser_random_api():
    """Hot User Recom Score 랜덤 가중치 조절"""
    hotuser_random = MasterConfig().get_config('hotuser_random')
    hotuser_random = hotuser_random['value'] if hotuser_random else 0.5
    return response_200(hotuser_random or 0.5)


@api.put('/admin/hotuser-random')
@Validator(bad_request)
@timer
def put_hotuser_random_api(
    value=Query([float, int])
):
    """Hot User Recom Score 랜덤 가중치 조절"""
    MasterConfig().set_config('hotuser_random', value)
    return response_200()


@api.get('/admin/topic-similarity')
@Validator(bad_request)
@timer
def get_topic_similarity_api():
    """Topic Model 유사도 가중치 조절"""
    topic_similarity = MasterConfig().get_config('topic_similarity')
    topic_similarity = topic_similarity['value'] if topic_similarity else 1
    return response_200(topic_similarity or 1)


@api.put('/admin/topic-similarity')
@Validator(bad_request)
@timer
def put_topic_similarity_api(
    value=Query([float, int])
):
    """Topic Model 유사도 가중치 조절"""
    MasterConfig().set_config('topic_similarity', value)
    return response_200()


@api.get('/admin/cold-to-hot')
@Validator(bad_request)
@timer
def get_cold_to_hot_api():
    """Cold to Hot 유저 변경 기준 조절"""
    cold_to_hot = MasterConfig().get_config('cold_to_hot')
    cold_to_hot = cold_to_hot['value'] if cold_to_hot else 10
    return response_200(cold_to_hot or 10)


@api.put('/admin/cold-to-hot')
@Validator(bad_request)
@timer
def put_cold_to_hot_api(
    value=Query(int)
):
    """Cold to Hot 유저 변경 기준 조절"""
    MasterConfig().set_config('cold_to_hot', value)
    return response_200()