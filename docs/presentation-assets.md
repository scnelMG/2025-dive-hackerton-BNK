# README 시각 자료 출처

README에 삽입한 시각 자료는 모두 프로젝트에서 실제로 사용하거나 분석 노트북에 저장된 산출물입니다. 별도로 생성·합성한 이미지는 사용하지 않았습니다.

| README 파일 | 원본 | 내용 |
| --- | --- | --- |
| `assets/presentation/two-track-framework.png` | `IBA_서호영.pptx` 4쪽 | 이자이익·비이자이익 Two-track 분석 프레임 |
| `assets/presentation/noninterest-growth-roadmap.png` | `IBA_서호영.pptx` 12쪽 | 비이자이익 성장 사다리와 교차 확장 전략 |
| `assets/presentation/loan-targeting-strategy.png` | `IBA_서호영.pptx` 23쪽 | 서민전용대출 잠재고객 발굴·관리 전략 |
| `assets/analysis/noninterest-elbow-k4.png` | `notebooks/1.전처리_및_군집화.ipynb`에 저장된 실제 출력 | 비이자이익 K-Means 군집 수 선택의 elbow 결과. `Best k=4` 표기가 있는 당시 분석 출력 |

발표자료 원본은 [IBA_서호영.pptx](IBA_서호영.pptx)에서 직접 확인할 수 있습니다. README의 군집별 인원·비중은 `noninterest-growth-roadmap.png`와 같은 **12쪽**을 출처로 합니다. `63%`처럼 원본 슬라이드에서 정확한 위치를 확인하지 못한 수치는 README에서 제거했습니다.

`noninterest-elbow-k4.png`는 원본 고객 데이터를 다시 실행해 만든 그림이 아닙니다. 공개된 분석 노트북에 이미 저장되어 있던 출력에서 추출한 이미지이며, 파일 SHA-256은 `A17996F0598B8D2EDB57D69446BE3A3424F0460E4A0054F27E5F86046F007C20`입니다. 이 결과는 당시 `k=4` 선택의 근거를 보여주지만 silhouette, 안정성 검증, 재현 실행을 대신하지는 않습니다.
