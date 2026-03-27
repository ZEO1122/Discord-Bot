---
briefing_key: "dl-concept-041-pretraining"
track: "dl-basics"
mode: "concept"
title: "사전학습"
one_line: "사전학습은 큰 데이터와 일반적인 목표로 먼저 학습해 넓은 패턴을 익히는 단계다."
discussion_prompt: "목표 과제를 바로 배우지 않고 먼저 넓은 데이터로 준비 운동을 하는 방식이 왜 강력할까?"
---

## 핵심 설명
- 사전학습은 대규모 데이터에서 비교적 일반적인 목표를 사용해 모델이 기본 표현을 먼저 익히게 하는 과정이다.
- 이 단계에서 모델은 언어 규칙, 시각적 패턴, 구조적 통계처럼 여러 과제에 재사용 가능한 지식을 배울 수 있다.
- 이후 특정 과제용 데이터가 적더라도, 사전학습된 표현을 바탕으로 더 빠르고 안정적으로 적응할 수 있다.
- 현대 대형 언어 모델과 비전 모델의 성능 향상에서 사전학습은 매우 중요한 기반이 되었다.

## 직관
- 전문 훈련 전에 넓은 기초 체력을 먼저 쌓아 두는 것과 비슷하다.
- 새 도시에서 길찾기를 배우기 전에 지도를 읽는 일반 원리를 먼저 익히는 과정으로 생각할 수 있다.

## 헷갈리기 쉬운 점
- 사전학습이 곧 특정 과제 성능을 보장하는 것은 아니다. 목표 과제에 맞는 추가 조정이 여전히 필요할 수 있다.
- 사전학습은 단순히 더 오래 학습하는 것과 다르다. 일반적 목표와 큰 데이터로 재사용 가능한 표현을 만든다는 점이 핵심이다.

## 셀프 체크 퀴즈
1. 사전학습은 어떤 종류의 지식을 먼저 익히게 하는가?
2. 사전학습된 모델이 적은 데이터 환경에서 유리한 이유는 무엇인가?
3. 사전학습과 단순 장시간 학습을 구분해야 하는 이유는 무엇인가?

## source
- Dumitru Erhan et al. / Why Does Unsupervised Pre-training Help Deep Learning? / 2010
- Jacob Devlin et al. / BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding / 2019
- Ian Goodfellow, Yoshua Bengio, Aaron Courville / Deep Learning / 2016