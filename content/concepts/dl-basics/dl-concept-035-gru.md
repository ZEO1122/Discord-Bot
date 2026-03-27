---
briefing_key: "dl-concept-035-gru"
track: "dl-basics"
mode: "concept"
title: "GRU"
one_line: "GRU는 LSTM보다 간단한 게이트 구조로 시퀀스 의존관계를 학습하는 순환신경망이다."
discussion_prompt: "비슷한 목적을 가지면서도 구조를 더 단순하게 만든 GRU는 어떤 상황에서 매력적일까?"
---

## 핵심 설명
- GRU(Gated Recurrent Unit)는 업데이트 게이트와 리셋 게이트를 사용해 정보 유지와 갱신을 조절한다.
- LSTM보다 구조가 단순해 파라미터 수가 적고 계산이 가벼운 편이다. 그럼에도 긴 의존관계를 다루는 능력을 상당 부분 유지한다.
- 데이터 크기, 과제 특성, 자원 제약에 따라 LSTM보다 더 실용적인 선택이 될 수 있다.
- 결국 GRU와 LSTM의 우열은 절대적이지 않다. 실제 성능과 효율을 함께 비교해 선택하는 경우가 많다.

## 직관
- 복잡한 서류 보관함 대신, 자주 쓰는 두 개 버튼만 있는 간단한 정리함으로도 충분히 일을 잘할 수 있는 상황과 비슷하다.
- 자동차의 기능을 줄였지만 핵심 주행 성능은 유지한 경량 모델처럼 생각할 수 있다.

## 헷갈리기 쉬운 점
- GRU가 LSTM보다 단순하다고 해서 항상 성능이 낮은 것은 아니다. 어떤 데이터에서는 비슷하거나 더 잘 작동할 수도 있다.
- 게이트 구조가 단순해도 기본 RNN보다 훨씬 안정적일 수 있다. 단순함과 약함은 같은 뜻이 아니다.

## 셀프 체크 퀴즈
1. GRU가 LSTM보다 구조적으로 단순한 이유는 무엇인가?
2. GRU가 실무에서 매력적인 선택이 될 수 있는 이유는 무엇인가?
3. GRU와 LSTM 중 어느 쪽이 더 낫다고 일반화하기 어려운 이유는 무엇인가?

## source
- Kyunghyun Cho et al. / Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation / 2014
- Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola / Dive into Deep Learning
- Stanford / CS224n Sequence Modeling Materials