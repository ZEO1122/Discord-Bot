---
briefing_key: "dl-concept-048-diffusion-model"
track: "dl-basics"
mode: "concept"
title: "확산모델"
one_line: "확산모델은 데이터에 점차 노이즈를 더하는 과정을 거꾸로 되돌리며 샘플을 생성하는 모델이다."
discussion_prompt: "데이터를 한 번에 만들어 내지 않고 노이즈 제거를 여러 단계로 나누는 방식은 어떤 장점을 가질까?"
---

## 핵심 설명
- 확산모델은 먼저 데이터에 조금씩 노이즈를 더해 결국 순수한 잡음에 가깝게 만든다고 가정한다. 그런 뒤 학습을 통해 이 과정을 역으로 되돌리는 법을 배운다.
- 생성 단계에서는 무작위 노이즈에서 출발해 여러 번의 복원 단계를 거치며 점점 의미 있는 샘플을 만든다.
- 복잡한 분포를 단계적으로 다루기 때문에 고품질 생성이 가능하다는 장점이 있다. 최근 이미지 생성에서 강력한 성능을 보였다.
- 다만 샘플 생성에 여러 단계가 필요해 속도가 느릴 수 있고, 이를 줄이기 위한 다양한 개선이 연구되었다.

## 직관
- 안개가 낀 사진을 한 번에 선명하게 만드는 대신, 조금씩 잡음을 걷어 내며 그림을 드러내는 방식과 비슷하다.
- 조각상을 한 번에 깎아 내는 대신, 덮인 먼지를 여러 번 털어 내며 형태를 드러내는 과정으로 생각할 수 있다.

## 헷갈리기 쉬운 점
- 확산모델은 단순한 잡음 제거기와 같지 않다. 데이터 분포에서 새로운 샘플을 생성하도록 전체 역과정을 학습한다.
- 여러 단계를 거친다고 해서 무조건 더 좋은 것은 아니다. 품질과 속도 사이의 균형이 중요한 모델 계열이다.

## 셀프 체크 퀴즈
1. 확산모델에서 학습하는 역과정은 무엇을 의미하는가?
2. 확산모델이 노이즈에서 시작해 샘플을 생성할 수 있는 이유는 무엇인가?
3. 확산모델의 대표적인 단점으로 속도가 언급되는 이유는 무엇인가?

## source
- Jascha Sohl-Dickstein et al. / Deep Unsupervised Learning using Nonequilibrium Thermodynamics / 2015
- Jonathan Ho, Ajay Jain, Pieter Abbeel / Denoising Diffusion Probabilistic Models / 2020
- Yang Song et al. / Score-Based Generative Modeling through Stochastic Differential Equations / 2021