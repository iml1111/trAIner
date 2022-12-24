
# trAIner - AI 알고리즘 학습 플랫폼
2022년 2학기 세종대학교 캡스톤 프로젝트 - trAIner
![image](https://user-images.githubusercontent.com/29897277/208664623-e24e991e-6693-4f46-b904-4c40571d9980.png)
 **trAIner(트레이너)는** 학습자의 관심도, 취약점 패턴을 분석하여 사용자가 좀 더 효율적으로 학습할 수 있도록 **알고리즘 문제를 추천해주는 AI 기반의 학습 플랫폼**입니다.

### key points
🚩**AI 추천 시스템을 통한 개인화된 맞춤 로드맵 생성**
🚩**토픽 모델링을 통한 알고리즘 문제 유형 분류 제공**
🚩**사용자의 상호작용 데이터 수집 및 전이학습 수행**

## trAIner 소개
![image](https://user-images.githubusercontent.com/29897277/208668718-85373146-6d3a-4fac-815e-073d94b78aaa.png)

트레이너는 자연어처리(NLP), Factorization Machine 기반의 딥러닝 기술을 통해 사용자와 알고리즘 문제 사이의 상관관계를 분석합니다. 유저들의 각 문제에 대한 **클릭률(CTR), 취약점(Vulnerability), 관심사(Topic)** 정보를 예측하여 각 사용자들에게 최적의 학습 문제를 추천할 수 있습니다.
![제목 없음](https://user-images.githubusercontent.com/29897277/208671083-b2fa4cea-bdff-4440-abef-29f83b3e3df6.png)

## trAIner 추천 시스템
트레이너의 추천 시스템은 사용자마다 다를 수 있는 개인차를 고려하여, 최대한 다양한 추천 패턴을 기능으로 제공할 수 있도록 시스템을 설계하였습니다. **클릭률, 취약점, 주제 분석 등 총 3개의 AI 모델을 채택**하여 최대 10개가 넘는 AI 기반의 예측 피드를 사용자에게 제공합니다.
### Matrix Factorization (CTR Prediction)
![image](https://user-images.githubusercontent.com/29897277/208677868-4caa9404-536b-4e46-8de1-4fc36fac0112.png)
- 관련 문헌: [Matrix Factorization Techniques for Recommender Systems](https://datajobs.com/data-science-repo/Recommender-Systems-%5bNetflix%5d.pdf)

Matrix Factorization(MF)는 Collaborative Filtering 방법론 중 하나로, 사용자와 아이템 간의 평가 정보를 나타내는 Rating Matrix를 기반으로 User Latent Matrix와 Item Latent Matrix로 분해하는 기법입니다. 이를 통해 문제에 대한 각 사용자에 대하여 특정 임계치를 기준으로 클릭 유무에 대한 True|False를 예측합니다. MF 모델의 최종 학습을 기준으로 한 평가 지표는 아래와 같습니다.

- **Train RMSE Loss: 0.674447**
- **Test RMSE Loss: 1.0221295**
- **Accuracy: 90.6476%**

**Confusion Matrix**는 다음과 같습니다.
||Positivie|Negative|
|------|---|---|
|**Positivie**|535,632|77,582|
|**Negative**|85,961|624,799|


### DeepFM (Vulnerity Prediction)
![image](https://user-images.githubusercontent.com/29897277/208679749-ecba1f87-bb87-4ece-b480-65161132de20.png)

- 관련 문헌: [DeepFM:A Factorization-Machine based Neural Network for CTR Prediction](https://arxiv.org/pdf/1703.04247.pdf)

Deep Factorization-Machine(DeepFM)은 2017년에 공개된 딥러닝 기반의 추천 시스템 구현을 위해 제안된 신경망으로 기존에 구글에서 발표했던 Wide & Deep Model의 잦은 Feature Engineering(피쳐 엔지니어링) 대한 단점을 보완하면서 해당 장점을 가져오기 위해 구현된 모델입니다.

트레이너에서 정의한 사용자의 취약점이라는 비교적 복잡한 Feature를 해석하고 예측하기 위해 본 모델을 채택하여 사용하였습니다.

**평가 지표**
- **Vulnerability Range: 0 ~ 1**
- **Train RMSE Loss: 2.5728e-05**
- **Test RMSE Loss: .27526e-05**

### Word2Vec (Topic Embedding)
![image](https://user-images.githubusercontent.com/29897277/208681882-7330e06d-76e6-4c80-9d3f-e2b89c0b374b.png)

- 관련 문헌: [Efficient Estimation of Word Representations in Vector Space](https://arxiv.org/pdf/1301.3781.pdf)

워드투벡터는 기존 자연어처리(NLP) 분야에서 One-Hot 벡터와 같은 descrete한 벡터들 사이에서 유사도를 계산하기 위해 만들어진 다양한 방법 중 하나입니다. 트레이너는 이러한 기법을 추천 시스템에 적용하여 유사한 알고리즘을 가진 문제들 사이의 관계를 수치화하여 비슷한 유형, 패턴을 가지는 문제들을 추천할 수 있습니다.

# 서비스 구조도
## 전체 구성도 & 백그라운드 사용자 분석 프로세스
![image](https://user-images.githubusercontent.com/29897277/208671733-5f960cc2-3ee5-4aca-9a1c-bb2b240ca743.png)
### 사용자 데이터 전처리 및 모델 전이 학습
![image](https://user-images.githubusercontent.com/29897277/208671864-d32c0577-09bf-4aaa-a5d5-599527fd307f.png)
## 인프라 구조도
![image](https://user-images.githubusercontent.com/29897277/208672140-a0929a2c-f5c1-4539-aafb-6b0ddf872a26.png)

