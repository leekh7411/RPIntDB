
***RNA Protein Interaction(RPI) Database***
# **RPIntDB**
![RNA Protein 결합 예시](http://swift-lang.org/case_studies/images/rna.png)

RNA와 Protein의 상호작용(Interaction) 혹은 결합 유무를 판단하기 위해 수집된 데이터베이스. RPI 연구분야에서 머신러닝을 사용하는 경우 Classification문제에 적용하여 분석을 수행해오고 있다. 여기서는 벤치마크 데이터로 사용되는 5가지 RPI 데이터셋에 대한 전처리과정을 코드로 제공하고 있다

## About the Raw Data
`data/` 폴더에 있는 RPI 데이터셋(`RPI1807_pairs.txt, NPInter_pairs.txt, etc..`)은 레퍼런스 ID 쌍과 결합 여부(0,1) 총 3개 탭으로 하나의 데이터를 제공하고 있다. 여기서는 시퀀스 기반 데이터셋으로 전처리 하기위해 PDB 등 외부 RPI 데이터베이스로부터 얻어진 각 ID의 시퀀스를  `data/sequence` 폴더에 개별로 저장해 관리한다. `data/structure` 폴더에는 각 ID 값에 해당하는 RNA 혹은 Protein 시퀀스의 2차구조를 저장하고 있다.  현재 제공되는 코드에는 structure 정보에 대한 전처리는 포함되어 있지 않다

### Usage
`rawdata_preprocessing.py` 에서는 앞서 설명된 pair 데이터를 읽고 sequence를 참조하여 Python 자료형으로 read할 수 있는 함수들을 제공하고 있다

## Feature Preprocessing
![reduced Protein에 대한 CTF 예시](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSC2ecLGlTSPxoi4pm3YkgeXdOMi7U5A6CXtKaKrik4kOW1WcPs)

2019년에 소개된 연구[1]에서 소개하는 전처리 기법을 `feature_preprocessing.py` 에서 일부 사용하고 있다. RPI연구 혹은 Bioinformatics분야에서 시퀀스 데이터를 처리하기 위해 많이 사용되는 기법인 CTF(Conjoint Triad Feature)를 사용한다. CTF는 연속된 시퀀스 3개의 패턴을 모두 저장해 시퀀스 데이터에서 일종의 패턴 분포를 표현하는 방식이다. 

[1]의 연구에서는 improved CTF를 사용하였는데 이는 3개의 패턴이 아닌 1-4개(RNA) 혹은 1-3개(reduced Protein) 패턴 분포를 모두 저장하는 방식이다. 해당 코드에서 사용한 방식은 improved CTF이다

### Usage
전처리 과정을 수행하는 `feature_preprocessing.py` 을 실행하면 5개의 벤치마크 데이터셋이 npz파일로 전처리되어 저장된다 

## RPI Classification (실습 과제)
RPI classification을 수행하기 위해서는 저장된 npz 파일을 불러오고 원하는 classification 모델을 선택한 다음 평가를 진행해야한다. 프로그래밍으로 직접 수행해야할 목록은 다음과 같다

1. 전처리 과정을 수행하여 npz타입으로 저장된 파일을 읽기
2. 학습데이터셋과 평가용 데이터셋을 분리 **(ex. RPI2241은 학습용, RPI369는 평가용)**
3. Binary classification 모델을 선택 **(ex. Random Forest, Support Vector Machine, ...)**
4. 학습된 모델과 테스트 데이터셋을 사용하여 성능 평가

아래는 실습을 위한 참고자료 입니다.

-  [Python에서 Random Forest(Scikit-learn) 모델 사용하기](https://scikit-learn.org/stable/modules/ensemble.html#forests-of-randomized-trees)
- [Python에서 Support Vector Machine 모델 사용하기](https://scikit-learn.org/stable/modules/svm.html#classification)
- [Classification결과를 간단히 확인하기(with Test set)](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.classification_report.html)


## References

[1] [https://github.com/Pengeace/RPITER](https://github.com/Pengeace/RPITER)
[2] PEDREGOSA, Fabian, et al. Scikit-learn: Machine learning in Python. _Journal of machine learning research_, 2011, 12.Oct: 2825-2830.