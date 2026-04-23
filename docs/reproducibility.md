# 재현 가이드

## 먼저 알아둘 점

이 저장소는 공개 포트폴리오용으로 정리된 버전입니다.  
대회 제공 원본 데이터와 일부 참고 자료는 포함하지 않으므로, 저장소만으로 전체 분석을 완전히 재실행할 수는 없습니다.

대신 아래는 확인할 수 있습니다.

- 분석 흐름
- 전처리 방식
- 군집화와 해석 구조
- 전략 제안의 연결 방식

## 권장 확인 순서

1. [../README.md](../README.md)
2. [project-summary.md](project-summary.md)
3. [analysis-method.md](analysis-method.md)
4. [results.md](results.md)
5. [../notebooks/1.전처리_및_군집화.ipynb](../notebooks/1.전처리_및_군집화.ipynb)
6. [../notebooks/2.비이자이익_분석.ipynb](../notebooks/2.비이자이익_분석.ipynb)
7. [../notebooks/3.이자이익_분석.ipynb](../notebooks/3.이자이익_분석.ipynb)

## 필요한 입력 데이터

원본 노트북은 대회 제공 데이터와 일부 파생 파일을 참조합니다.  
포트폴리오 저장소에는 해당 파일을 포함하지 않았습니다.

당시 사용한 입력 자료 유형은 아래와 같습니다.

- 고객 원천 데이터 CSV
- 데이터 명세 XLSX
- 전처리 후 파생 파일

## 데이터를 포함하지 않은 이유

- 대회 제공 자료의 재배포 권한이 불명확함
- 금융 고객 데이터 특성상 공개 저장소 업로드가 적절하지 않음
- 포트폴리오 목적상 데이터 자체보다 분석 구조와 해석 역량을 보여주는 편이 중요함

자세한 공개 기준은 [../data/README.md](../data/README.md)에서 확인할 수 있습니다.

## 실행 환경

- Python 3.9+
- Jupyter Notebook 또는 JupyterLab
- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn

의존성 설치는 루트의 [../requirements.txt](../requirements.txt)를 참고하면 됩니다.

## 실행 시 유의 사항

- 일부 노트북은 해커톤 제출 환경 기준으로 작성되어 경로 설정이 로컬 환경에 의존할 수 있습니다.
- 폰트, 파일 경로, 출력 셀 순서는 사용자 환경에서 다르게 보일 수 있습니다.
- 원본 데이터가 없으면 전체 재실행은 어렵지만, 분석 흐름과 판단 근거는 코드와 문서로 확인할 수 있습니다.
