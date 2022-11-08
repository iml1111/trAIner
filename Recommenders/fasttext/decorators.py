from datetime import datetime


# 모듈 시간 측정 함수
def timer(f):
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        result = f(*args, **kwargs)
        end_time = datetime.now()
        print("Total Train Time:",end_time-start_time)
        return result
    return wrapper


# 학습 관련 데코레이터
def train_deco(f):
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        print("Model Train Start >",start_time)
        result = f(*args, **kwargs)
        end_time = datetime.now()
        print("Model Train Complete >",end_time)
        return result
    return wrapper


# 전이학습 관련 데코레이터
def update_deco(f):
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        print("Model Update Start >",start_time)
        result = f(*args, **kwargs)
        end_time = datetime.now()
        print("Model Update Complete >",end_time)
        return result
    return wrapper


# 모델이 필요한 메소드시, 검증
def model_require(f):
    def wrapper(*args, **kwargs):
        if args[0].model is None:
            raise RuntimeError("Model is 'None'")
        return f(*args, **kwargs)
    return wrapper