---
briefing_key: "dl-concept-040-encoder-decoder"
track: "dl-basics"
mode: "concept"
title: "인코더-디코더 구조"
one_line: "인코더-디코더 구조는 입력을 표현으로 바꾼 뒤 그 표현을 바탕으로 출력을 생성하는 틀이다."
discussion_prompt: "입력을 이해하는 단계와 출력을 만들어 내는 단계를 나누면 어떤 종류의 문제를 더 잘 다룰 수 있을까?"
---

## 핵심 설명
- 인코더는 입력 시퀀스나 데이터를 받아 의미 있는 내부 표현으로 바꾼다. 디코더는 그 표현을 바탕으로 원하는 출력 시퀀스를 생성한다.
- 입력과 출력의 길이가 다를 수 있는 문제에 특히 잘 맞는다. 번역, 요약, 음성 인식, 이미지 캡셔닝이 대표적이다.
- 초기에는 RNN 기반 구조가 많았고, 이후 어텐션과 트랜스포머 기반 인코더-디코더가 널리 쓰였다.
- 핵심 아이디어는 이해와 생성의 역할을 분리해, 입력을 해석한 뒤 그 정보를 활용해 출력을 순차적으로 만들게 하는 것이다.

## 직관
- 통역사가 먼저 원문을 이해하고 머릿속에 정리한 뒤, 그것을 다른 언어로 말해 주는 과정과 비슷하다.
- 요리법을 읽고 핵심을 머릿속에 정리한 다음, 실제 요리를 차례대로 만들어 내는 흐름으로 볼 수 있다.

## 헷갈리기 쉬운 점
- 인코더가 반드시 하나의 고정 길이 벡터만 만들어야 하는 것은 아니다. 어텐션 이후에는 입력의 여러 위치 표현을 계속 참조할 수 있다.
- 디코더는 단순한 출력층이 아니다. 이전에 생성한 결과와 인코더 정보를 함께 보며 다음 출력을 결정하는 구조일 수 있다.

## 셀프 체크 퀴즈
1. 인코더와 디코더는 각각 어떤 역할을 하는가?
2. 입력과 출력 길이가 다른 문제에서 인코더-디코더 구조가 유용한 이유는 무엇인가?
3. 어텐션이 인코더-디코더 구조를 더 강력하게 만든 이유는 무엇인가?

## source
- Ilya Sutskever, Oriol Vinyals, Quoc V. Le / Sequence to Sequence Learning with Neural Networks / 2014
- Dzmitry Bahdanau, Kyunghyun Cho, Yoshua Bengio / Neural Machine Translation by Jointly Learning to Align and Translate / 2015
- Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola / Dive into Deep Learning