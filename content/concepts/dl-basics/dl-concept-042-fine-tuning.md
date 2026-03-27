---
briefing_key: "dl-concept-042-fine-tuning"
track: "dl-basics"
mode: "concept"
title: "미세조정"
one_line: "미세조정은 사전학습된 모델을 특정 과제와 데이터에 맞게 추가로 학습시키는 과정이다."
discussion_prompt: "이미 많은 지식을 가진 모델도 왜 목표 과제에 맞는 마지막 조정이 필요할까?"
---

## 핵심 설명
- 미세조정은 사전학습 모델의 파라미터를 초기값으로 사용하고, 목표 과제 데이터로 추가 학습하는 방법이다.
- 사전학습이 일반적인 패턴을 익혔다면, 미세조정은 그 지식을 특정 도메인과 출력 형식에 맞게 다듬는 단계다.
- 전체 파라미터를 모두 조정할 수도 있고, 일부 층만 조정하거나 작은 추가 모듈만 학습할 수도 있다.
- 적은 데이터로도 좋은 출발점을 활용할 수 있어 학습 효율을 높이는 데 매우 유용하다.

## 직관
- 기초 영어를 잘하는 사람이 법률 영어 수업을 추가로 들으며 표현을 다듬는 과정과 비슷하다.
- 이미 기본 지도가 있는 내비게이션에 지역별 상세 정보를 업데이트하는 작업으로 생각할 수 있다.

## 헷갈리기 쉬운 점
- 미세조정은 모델을 처음부터 다시 학습하는 것과 다르다. 기존 지식을 활용해 목표 과제에 맞게 수정한다.
- 전체를 모두 업데이트해야만 미세조정인 것은 아니다. 일부만 조정하는 방식도 넓은 의미의 미세조정에 포함된다.

## 셀프 체크 퀴즈
1. 미세조정은 사전학습과 어떤 관계를 가지는가?
2. 미세조정에서 일부 층만 조정하는 전략을 사용할 수 있는 이유는 무엇인가?
3. 적은 데이터에서 미세조정이 유리한 이유는 무엇인가?

## source
- Jacob Devlin et al. / BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding / 2019
- Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola / Dive into Deep Learning
- Stanford / CS224n Transfer Learning and Fine-tuning Materials