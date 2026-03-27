---
briefing_key: "dl-concept-017-weight-initialization"
track: "dl-basics"
mode: "concept"
title: "가중치 초기화"
one_line: "가중치 초기화는 학습 시작점의 파라미터 값을 정해 기울기 흐름과 학습 안정성에 큰 영향을 준다."
discussion_prompt: "학습은 결국 데이터를 보고 바뀌는 과정인데도 시작값이 중요한 이유는 무엇일까?"
---

## 핵심 설명
- 가중치 초기화는 학습 전에 파라미터를 어떤 값으로 시작할지 정하는 일이다. 시작점이 다르면 학습 경로와 수렴 속도가 달라질 수 있다.
- 모든 가중치를 같은 값으로 두면 뉴런들이 같은 일을 하게 되어 대칭성이 깨지지 않는다. 그래서 보통 작은 무작위 값으로 초기화한다.
- 너무 큰 값이나 너무 작은 값은 층을 거치며 신호와 기울기를 폭발시키거나 사라지게 만들 수 있다. Xavier 초기화와 He 초기화는 이런 문제를 완화하려는 대표 방법이다.
- 초기화는 단순 준비 단계가 아니라, 깊은 네트워크가 실제로 학습되게 만드는 핵심 조건 중 하나다.

## 직관
- 여러 사람이 같은 출발선에서 똑같은 방향만 보면 협업이 안 되듯이, 뉴런도 처음부터 조금씩 다른 역할을 시작해야 한다.
- 건물을 세울 때 기초가 기울어 있으면 위층 공사가 어려워지는 것처럼, 초기화가 나쁘면 뒤 학습이 힘들어진다.

## 헷갈리기 쉬운 점
- 가중치를 0으로 시작하면 깔끔해 보이지만 대부분의 층에서 좋지 않다. 뉴런들이 서로 구별되지 않기 때문이다.
- 좋은 초기화가 학습을 대신해 주는 것은 아니다. 다만 학습이 가능하고 안정적으로 진행되도록 돕는다.

## 셀프 체크 퀴즈
1. 모든 가중치를 같은 값으로 초기화하면 왜 문제가 생길 수 있는가?
2. 가중치 초기화가 기울기 소실이나 폭발과 연결되는 이유는 무엇인가?
3. Xavier 초기화와 He 초기화는 어떤 문제를 완화하려는가?

## source
- Xavier Glorot, Yoshua Bengio / Understanding the Difficulty of Training Deep Feedforward Neural Networks / 2010
- Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun / Delving Deep into Rectifiers / 2015
- Ian Goodfellow, Yoshua Bengio, Aaron Courville / Deep Learning / 2016