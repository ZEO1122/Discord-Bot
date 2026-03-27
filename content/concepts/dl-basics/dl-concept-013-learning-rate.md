---
briefing_key: "dl-concept-013-learning-rate"
track: "dl-basics"
mode: "concept"
title: "학습률"
one_line: "학습률은 한 번의 업데이트에서 파라미터를 얼마나 크게 움직일지를 정하는 핵심 하이퍼파라미터다."
discussion_prompt: "모델 구조가 좋아도 학습률 설정이 잘못되면 학습이 무너질 수 있는 이유는 무엇일까?"
---

## 핵심 설명
- 학습률은 기울기 방향으로 얼마만큼 이동할지 정하는 계수다. 같은 기울기라도 학습률이 다르면 업데이트 크기가 달라진다.
- 값이 너무 크면 최솟값 근처를 지나치거나 발산할 수 있다. 반대로 너무 작으면 학습이 매우 느리거나 좋은 지점에 도달하기 전에 멈춘 것처럼 보일 수 있다.
- 학습 초반과 후반에 서로 다른 학습률이 더 적합할 수 있다. 그래서 스케줄링이나 warmup 같은 기법이 함께 사용되기도 한다.
- 학습률은 옵티마이저, 배치 크기, 정규화 방식과 상호작용한다. 단독 숫자 하나가 아니라 전체 학습 전략의 일부다.

## 직관
- 계단을 내려갈 때 보폭이 너무 크면 헛디디고, 너무 작으면 오래 걸린다. 학습률은 그 보폭과 비슷하다.
- 차를 주차할 때 한 번에 너무 많이 꺾으면 지나치고, 너무 조금 움직이면 제자리에서만 수정하는 상황과 닮아 있다.

## 헷갈리기 쉬운 점
- 학습률이 작다고 해서 항상 안전한 것은 아니다. 너무 작으면 사실상 학습이 거의 진행되지 않는다.
- 좋은 학습률은 데이터셋마다 다를 수 있다. 다른 실험의 숫자를 그대로 가져오면 잘 맞지 않을 수 있다.

## 셀프 체크 퀴즈
1. 학습률이 너무 크면 왜 발산이나 진동이 생길 수 있는가?
2. 학습률이 너무 작을 때 학습이 느려지는 이유는 무엇인가?
3. 학습률 스케줄링이 필요한 상황은 어떤 경우인가?

## source
- Ian Goodfellow, Yoshua Bengio, Aaron Courville / Deep Learning / 2016
- Léon Bottou, Frank E. Curtis, Jorge Nocedal / Optimization Methods for Large-Scale Machine Learning / 2018
- Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola / Dive into Deep Learning