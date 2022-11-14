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
    return response_200(ctr_threshold or 3)


@api.put('/admin/ctr-threshold')
@Validator(bad_request)
@timer
def put_ctr_threshold_api(
    threshold=Query([float, int])
):
    """CTR Model 기준 임계치 파라미터 조절"""
    MasterConfig().set_config('ctr_threshold', threshold)
    return response_200()


@api.get('/admin/deep-threshold')
@Validator(bad_request)
@timer
def get_deep_threshold_api():
    """Deep Model 기준 임계치 파라미터 조절"""
    deep_threshold = MasterConfig().get_config('deep_threshold')
    return response_200(deep_threshold or 1)


@api.put('/admin/deep-threshold')
@Validator(bad_request)
@timer
def put_deep_threshold_api(
    threshold=Query([float, int])
):
    """Deep Model 기준 임계치 파라미터 조절"""
    MasterConfig().set_config('deep_threshold', threshold)
    return response_200()


@api.get('/admin/hotuser-random')
@Validator(bad_request)
@timer
def get_hotuser_random_api():
    """Hot User Recom Score 랜덤 가중치 조절"""
    hotuser_random = MasterConfig().get_config('hotuser_random')
    return response_200(hotuser_random or 0.5)


@api.put('/admin/hotuser-random')
@Validator(bad_request)
@timer
def put_hotuser_random_api(
    random=Query([float, int])
):
    """Hot User Recom Score 랜덤 가중치 조절"""
    MasterConfig().set_config('hotuser_random', random)
    return response_200()


@api.get('/admin/topic-similarity')
@Validator(bad_request)
@timer
def get_topic_similarity_api():
    """Topic Model 유사도 가중치 조절"""
    topic_similarity = MasterConfig().get_config('topic_similarity')
    return response_200(topic_similarity or 1)


@api.put('/admin/topic-similarity')
@Validator(bad_request)
@timer
def put_topic_similarity_api(
    similarity=Query([float, int])
):
    """Topic Model 유사도 가중치 조절"""
    MasterConfig().set_config('topic_similarity', similarity)
    return response_200()
