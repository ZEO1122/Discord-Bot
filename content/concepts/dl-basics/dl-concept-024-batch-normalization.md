---
briefing_key: "dl-concept-024-batch-normalization"
track: "dl-basics"
mode: "concept"
title: "배치 정규화"
one_line: "배치 정규화는 중간층의 활성값을 배치 기준으로 정규화해 학습을 더 안정적으로 만드는 기법이다."
discussion_prompt: "입력이 아니라 중간 표현을 정규화하는 방식이 왜 깊은 네트워크 학습에 도움이 될까?"
---

## 핵심 설명
- 배치 정규화는 층의 입력이나 활성값을 미니배치의 평균과 분산으로 정규화한 뒤, 다시 학습 가능한 스케일과 이동을 적용한다.
- 이 과정은 각 층으로 들어가는 값의 분포가 지나치게 흔들리는 것을 줄여, 더 큰 학습률에서도 안정적으로 학습되게 도울 수 있다.
- 배치 정규화는 종종 학습 속도를 높이고 초기화 민감도를 줄여 준다. 하지만 효과는 모델 구조와 배치 크기에 따라 달라진다.
- 추론 단계에서는 현재 배치 통계가 아니라 학습 중 누적한 평균과 분산을 사용한다는 점이 중요하다.

## 직관
- 조립 라인마다 들어오는 부품 크기를 비슷하게 맞춰 두면 다음 공정이 덜 흔들리는 것과 비슷하다.
- 각 반 학생의 점수를 바로 쓰지 않고 평균과 분산을 고려해 기준을 맞춘 뒤 평가하는 방식으로 이해할 수 있다.

## 헷갈리기 쉬운 점
- 배치 정규화는 과적합을 막는 정규화 효과가 일부 있을 수 있지만, 주목적은 학습 안정화다.
- 배치 크기가 매우 작으면 통계가 불안정해질 수 있다. 그래서 모든 상황에서 같은 효과를 기대하긴 어렵다.

## 셀프 체크 퀴즈
1. 배치 정규화는 각 층의 어떤 값을 정규화하는가?
2. 학습 단계와 추론 단계에서 사용하는 통계가 다른 이유는 무엇인가?
3. 배치 크기가 매우 작을 때 배치 정규화가 까다로울 수 있는 이유는 무엇인가?

## source
- Sergey Ioffe, Christian Szegedy / Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift / 2015
- Ian Goodfellow, Yoshua Bengio, Aaron Courville / Deep Learning / 2016
- Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola / Dive into Deep Learning