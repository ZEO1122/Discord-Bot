---
briefing_key: "dl-concept-044-self-supervised-learning"
track: "dl-basics"
mode: "concept"
title: "자기지도학습"
one_line: "자기지도학습은 데이터 자체에서 학습 목표를 만들어 레이블 없이 표현을 배우는 방법이다."
discussion_prompt: "정답 라벨이 없어도 데이터 안에서 학습 신호를 끌어낼 수 있다는 발상이 왜 중요한가?"
---

## 핵심 설명
- 자기지도학습은 사람이 붙인 정답 라벨 없이, 데이터 내부 구조를 이용해 예측 과제를 만든다. 가려진 단어 맞히기나 서로 맞는 짝 찾기가 대표적이다.
- 이 방식은 대규모 비라벨 데이터를 활용할 수 있어, 값비싼 수작업 라벨링의 부담을 크게 줄여 준다.
- 핵심 목표는 즉시 최종 과제를 푸는 것이 아니라, 이후 다양한 작업에 재사용 가능한 표현을 배우는 것이다.
- 현대 언어 모델과 많은 비전 모델의 기반 학습 전략으로 자기지도학습이 널리 사용된다.

## 직관
- 교사가 문제를 내주지 않아도, 책 일부를 가리고 다음 내용을 예측하며 스스로 공부하는 방식과 비슷하다.
- 퍼즐 조각의 일부를 숨기고 전체 그림을 유추하게 하는 연습으로 이해할 수 있다.

## 헷갈리기 쉬운 점
- 자기지도학습은 완전히 감독이 없는 무작위 학습이 아니다. 목표는 데이터에서 자동으로 만들지만, 분명한 학습 과제가 존재한다.
- 라벨이 없다고 해서 아무 정보도 없는 것은 아니다. 데이터의 순서, 구조, 짝 관계가 중요한 단서가 된다.

## 셀프 체크 퀴즈
1. 자기지도학습이 비라벨 데이터를 활용할 수 있는 이유는 무엇인가?
2. 가려진 단어 예측이 자기지도학습의 예가 되는 이유는 무엇인가?
3. 자기지도학습으로 얻은 표현이 이후 과제에 도움이 되는 이유는 무엇인가?

## source
- Ting Chen et al. / A Simple Framework for Contrastive Learning of Visual Representations / 2020
- Jacob Devlin et al. / BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding / 2019
- Longlong Jing, Yingli Tian / Self-supervised Visual Feature Learning with Deep Neural Networks: A Survey / 2020