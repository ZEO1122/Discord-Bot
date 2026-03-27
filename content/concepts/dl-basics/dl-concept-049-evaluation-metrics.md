---
briefing_key: "dl-concept-049-evaluation-metrics"
track: "dl-basics"
mode: "concept"
title: "평가 지표"
one_line: "평가 지표는 모델이 실제로 얼마나 잘 작동하는지 과제 목적에 맞게 수치로 판단하는 기준이다."
discussion_prompt: "손실이 아니라 평가 지표를 따로 챙겨야 하는 이유는 무엇일까?"
---

## 핵심 설명
- 평가 지표는 모델 성능을 해석하는 기준이다. 정확도, 정밀도, 재현율, F1, ROC-AUC, RMSE 같은 지표가 과제에 따라 사용된다.
- 좋은 지표는 실제 목표와 비용 구조를 반영해야 한다. 예를 들어 클래스 불균형이 심하면 정확도만으로는 성능을 오해할 수 있다.
- 손실 함수는 학습을 위한 내부 목표이고, 평가 지표는 결과를 판단하기 위한 외부 기준인 경우가 많다. 둘은 같을 수도 있지만 자주 다르다.
- 따라서 모델 비교에서는 숫자 하나만 보는 것이 아니라, 어떤 지표를 왜 선택했는지 함께 보는 태도가 중요하다.

## 직관
- 운동선수를 평가할 때 점수, 속도, 성공률을 종목별로 다르게 보는 것과 비슷하다. 한 숫자만으로는 충분하지 않다.
- 가게 운영을 볼 때 매출만이 아니라 이익, 재구매율, 반품률을 함께 보는 상황으로 생각할 수 있다.

## 헷갈리기 쉬운 점
- 정확도가 높다고 항상 좋은 모델은 아니다. 희귀 클래스가 중요한 문제에서는 정밀도나 재현율이 더 중요할 수 있다.
- 평가 지표는 많을수록 좋은 것이 아니다. 실제 목표와 가장 잘 맞는 지표를 중심으로 해석해야 한다.

## 셀프 체크 퀴즈
1. 손실 함수와 평가 지표를 구분해야 하는 이유는 무엇인가?
2. 클래스 불균형 문제에서 정확도만 보면 왜 오해가 생길 수 있는가?
3. 평가 지표를 선택할 때 실제 비용 구조를 고려해야 하는 이유는 무엇인가?

## source
- Ian Goodfellow, Yoshua Bengio, Aaron Courville / Deep Learning / 2016
- scikit-learn / Model Evaluation: Quantifying the Quality of Predictions
- Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola / Dive into Deep Learning