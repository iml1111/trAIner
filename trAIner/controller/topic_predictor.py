"""Topic Model Predictor Controller"""
import numpy as np
from gensim.models import Word2Vec
from gensim import matutils


class TopicPredictor:

    def __init__(self, topic_model_path: str):
        self.topic_model_path = topic_model_path
        self.model = Word2Vec.load(topic_model_path)

    def get_similar_items(self, item, num=10):
        """
        입력된 item에 대하여 가장 가까운 item를 n개 반환(복수도 가능.)
        Ex)
        item = "123"
        iteam = ["123", "456"]

        Return [
            # item, similarity
            ('989', 0.9443435668945312),
            ('862', 0.9233401417732239),
            ...
        ]
        """
        return self.model.wv.most_similar(item, topn=num)

    def get_similar_items_by_vector(self, vec, num=10):
        """
        입력된 item vector에 대하여 가장 가까운 item를 n개 반환
        """
        return self.model.wv.similar_by_vector(vec, topn=num)

    def item2vec(self, item: str):
        """입력된 item의 topic vector 반환"""
        if isinstance(item, str):
            item = [item]
        if item == []:
            raise RuntimeError("빈 리스트는 벡터화시킬 수 없습니다.")
        v = [self.model.wv[word] for word in item]
        return matutils.unitvec(np.array(v).mean(axis=0))

    def vec_sim(self, vec_A, vec_B):
        '''두 임베딩 벡터간의 의미적 유사도 반환'''
        return np.dot(vec_A, vec_B)

    def doc_sim(self, doc_A, doc_B):
        '''두 토큰 or 토큰 리스트에 대한 의미적 유사도 반환'''
        if isinstance(doc_A, str):
            doc_A = [doc_A]
        if isinstance(doc_B, str):
            doc_B = [doc_B]
        return self.model.wv.n_similarity(doc_A, doc_B)

    def is_in_dict(self, word):
        '''입력된 토큰이 모델이 알고 있는 토큰인지 반환'''
        return word in self.model.wv.key_to_index


if __name__ == '__main__':
    from config import config

    predictor = TopicPredictor(config.TOPIC_MODEL_PATH)

    # 해당 문제와 유사한 문제리스트 추출하기
    similar_801 = predictor.get_similar_items("801")
    print(similar_801)
    # 복수 문제들 집단에 대한 유사 리스트 추천도 가능
    similar_801_989 = predictor.get_similar_items(["801", "989"])
    print(similar_801_989)

    # 두 문제 사이의 유사도 측정하기 (벡터 뽑아서 측정하기, 다이렉트로 측정하기)
    vec_801 = predictor.item2vec("801")
    vec_989 = predictor.item2vec("989")
    print(predictor.vec_sim(vec_989, vec_801)) # maybe 0.9443...
    print(predictor.doc_sim("801", "989"))
    # 복수 문제 집단들에 대한 벡터 추출도 가능
    vec_801_989 = predictor.item2vec(["801", "989"])
    print(vec_801_989)

    # 해당 문제 index를 모델이 알고 있는지 확인하기
    print(predictor.is_in_dict("801"))
    # (주의!!) 절대로 문제 인덱스를 int로 입력해선 안됨!!
    print(predictor.is_in_dict(801))
    print(predictor.get_similar_items(801)) # << No Error