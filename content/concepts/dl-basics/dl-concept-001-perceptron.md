---
briefing_key: "dl-concept-001-perceptron"
track: "dl-basics"
mode: "concept"
title: "퍼셉트론"
one_line: "퍼셉트론은 입력의 가중합을 기준으로 두 범주를 나누는 가장 기본적인 인공 뉴런 모델이다."
discussion_prompt: "복잡한 신경망을 이해할 때 퍼셉트론의 단순한 결정 방식이 여전히 중요한 이유는 무엇일까?"
---

## 핵심 설명
- 퍼셉트론은 입력값에 가중치를 곱해 더한 뒤, 그 값이 기준을 넘는지에 따라 출력을 정하는 모델이다. 가장 단순한 이진 분류기의 형태로 볼 수 있다.
- 이 개념은 신경망이 입력을 선형 결합해 판단한다는 출발점을 보여 준다. 복잡한 모델도 기본적으로는 이런 연산을 여러 층에 걸쳐 반복한다.
- 한 개의 퍼셉트론은 직선이나 평면 같은 선형 경계만 만들 수 있다. 그래서 XOR처럼 선형적으로 나눌 수 없는 문제는 단독으로 풀기 어렵다.
- 퍼셉트론은 오늘날의 깊은 신경망보다 단순하지만, 가중치 학습과 결정 경계라는 핵심 아이디어를 이해하는 데 매우 유용하다.

## 직관
- 여러 개의 체크 항목에 점수를 매기고, 총점이 기준 이상이면 합격이라고 판단하는 방식과 비슷하다.
- 문 앞 경비원이 여러 조건을 빠르게 합쳐 들어올 수 있는지 없는지를 판단하는 규칙으로 생각할 수 있다.

## 헷갈리기 쉬운 점
- 퍼셉트론이 곧 모든 신경망을 뜻하는 것은 아니다. 퍼셉트론은 신경망을 이루는 아주 기본적인 출발점에 가깝다.
- 퍼셉트론이 학습한다고 해서 모든 패턴을 배울 수 있는 것은 아니다. 한 개의 퍼셉트론은 비선형 관계를 직접 표현하지 못한다.

## 셀프 체크 퀴즈
1. 퍼셉트론이 선형 분류기라고 불리는 이유는 무엇인가?
2. 한 개의 퍼셉트론으로 XOR 문제를 풀기 어려운 이유는 무엇인가?
3. 퍼셉트론에서 가중치와 기준값이 결정에 어떤 역할을 하는가?

## source
- Frank Rosenblatt / The Perceptron: A Probabilistic Model for Information Storage and Organization in the Brain / 1958
- Ian Goodfellow, Yoshua Bengio, Aaron Courville / Deep Learning / 2016
- Stanford / CS231n Course Notes on Linear Classification and Neural Networks