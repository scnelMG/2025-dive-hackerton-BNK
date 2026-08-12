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

원본 노트북은 저장소 루트 또는 `notebooks/` 폴더에서 열어도 `data/` 폴더를 찾도록 정리했습니다. 필요한 파일명은 다음과 같습니다.

- `notebooks/1.전처리_및_군집화.ipynb` → `./data/hacktho_FF.csv`
- `notebooks/2.비이자이익_분석.ipynb` → `./data/hacktho_FF_final.csv`
- `notebooks/3.이자이익_분석.ipynb` → `./data/hacktho_FF_final.csv`

해당 파일은 금융 고객 데이터로서 공개 저장소에 포함하지 않았습니다.

## 데이터를 포함하지 않은 이유

- 대회 제공 자료의 재배포 권한이 불명확함
- 금융 고객 데이터 특성상 공개 저장소 업로드가 적절하지 않음
- 포트폴리오 목적상 데이터 자체보다 분석 구조와 해석 역량을 보여주는 편이 중요함

자세한 공개 기준은 [../data/README.md](../data/README.md)에서 확인할 수 있습니다.

## 실행 환경

- Python 3.9+ (분석 노트북 기준)
- Python 3.10+ (`scripts/verify_portfolio.py` 실행 기준)
- Jupyter Notebook 또는 JupyterLab
- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn

의존성 설치는 루트의 [../requirements.txt](../requirements.txt)를 참고하면 됩니다. 전처리·군집화 노트북의 기록된 실행 환경은 Python 3.9.23이며, 나머지 노트북은 서로 다른 로컬 커널 기록을 가지고 있습니다. 정확한 당시 패키지 lockfile은 보존되지 않았으므로, 현재 `requirements.txt`는 분석 코드를 읽고 검토하기 위한 호환 범위입니다.

## 실행 시 유의 사항

- 노트북은 저장소 루트 또는 `notebooks/` 폴더에서 실행할 수 있도록 `data/` 위치를 계산합니다.
- 폰트, 파일 경로, 출력 셀 순서는 사용자 환경에서 다르게 보일 수 있습니다.
- 원본 데이터가 없으면 전체 재실행은 어렵지만, 분석 흐름과 판단 근거는 코드와 문서로 확인할 수 있습니다.

## 공개 저장소에서 검증 가능한 범위

원본 데이터 없이도 아래는 확인할 수 있습니다.

```bash
python scripts/verify_portfolio.py
```

이 명령은 필수 문서·README 구조·추적 파일 크기를 점검합니다. 이는 **분석 결과 재실행 검증이 아니라 공개 포트폴리오 구성 점검**입니다.
