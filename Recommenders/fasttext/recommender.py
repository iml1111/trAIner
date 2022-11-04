'''
FastText Recommender Module
'''
import numpy as np
from gensim.models import FastText
from gensim import matutils

class Recommender:
    '''FastText Recommender Class'''

    def __init__(self, path):
        self.model = FastText.load(path)

    def doc2words(self, doc, num=10):
        '''
        입력된 토큰, 토큰 리스트에 대하여
        가장 의미상 가까운 단어 num 개를 반환
        '''
        return self.model.wv.most_similar(doc, topn=num)

    def vec2words(self, vec, num=10):
        '''
        입력된 벡터에 대하여
        가장 의미상 가까운 단어 num 개를 반환
        '''
        return self.model.wv.similar_by_vector(vec, topn=num)

    def doc2vec(self, doc):
        '''입력된 토큰, 토큰 리스트에 대한 임베딩 벡터 반환'''
        if isinstance(doc, str):
            doc = [doc]
        if doc == []:
            raise RuntimeError("빈 리스트는 벡터화시킬 수 없습니다.")
        v = [self.model.wv[word] for word in doc]
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

    def make_test_report(self, path='./word_sim_test.md'):
        '''특정 키워드에 대한 모델 성능 측정 및 MD 문서화'''
        words = [str(i) for i in range(1000)]
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write("# 모델 단어 테스트\n\n")
            for ex in words:
                if not ex:
                    continue
                if not self.is_in_dict(ex):
                    print("Skipped:", ex)
                    continue
                f.write("### " + str(ex) + " \n")
                f.write(" **" + str(self.doc2words(ex)) + "** \n")
                f.write("\n")