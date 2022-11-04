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
        return word in self.model.wv.vocab

    def make_test_report(self, path='./word_sim_test.md'):
        '''특정 키워드에 대한 모델 성능 측정 및 MD 문서화'''
        words = [
            "공모전", "it", "컴퓨터", "취업", "진로", "장학",
            "근무", "학교", "공부", "용돈", "국제", "토익",
            "회계", "월급", "창업", "파이썬", "python", "java",
            "디자인", "웹", "영상", "디자이너", "구매", "상품",
            "데이터", "서버", "병원", "의료", "아르바이트", "연애",
            "자유", "일본", "코트", "칭찬", "동아리", "새내기", "영어",
            "채용", "학점", "수강", "생각", "스트레스", "행복", "수학",
            "elp", "교수", "과제", "수업", "점수", "출판", "선생님",
            "코딩", "물리", "군대", "대회", "세종대", "뉴스", "드라마",
            "소식", "작품", "교양", "세미나", "특강", "복학", "휴학",
            "장학금", "성적", "등록금", "질문", "후문", "학교", "알바",
            "선생", "과외", "과학"
        ]
        
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