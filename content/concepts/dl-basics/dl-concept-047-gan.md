---
briefing_key: "dl-concept-047-gan"
track: "dl-basics"
mode: "concept"
title: "생성적 적대 신경망"
one_line: "생성적 적대 신경망은 생성자와 판별자가 경쟁하며 점점 더 그럴듯한 데이터를 만드는 생성 모델이다."
discussion_prompt: "정답을 직접 맞추는 대신 서로 경쟁하는 두 모델을 붙이면 왜 강한 생성 능력이 생길까?"
---

## 핵심 설명
- GAN(Generative Adversarial Network)은 가짜 데이터를 만드는 생성자와, 진짜와 가짜를 구분하는 판별자가 함께 학습하는 구조다.
- 생성자는 판별자를 속이려 하고, 판별자는 이를 막으려 한다. 이 경쟁 과정에서 생성자는 점점 더 진짜 같은 샘플을 만들게 된다.
- GAN은 매우 선명한 이미지 생성으로 큰 주목을 받았지만, 학습이 불안정하고 모드 붕괴 같은 문제가 생기기 쉽다.
- 따라서 GAN은 강력하지만 다루기 까다로운 생성 모델로 자주 소개된다.

## 직관
- 위조지폐 제작자와 감별사가 서로 실력을 높여 가는 경쟁과 비슷하다.
- 모의 재판에서 공격과 방어가 모두 강해질수록 논리가 정교해지는 구조로 생각할 수 있다.

## 헷갈리기 쉬운 점
- GAN의 판별자는 최종 목적이 아니라 생성자를 훈련시키는 상대 역할이다. 학습 후에는 생성자만 사용하는 경우가 많다.
- GAN이 선명한 샘플을 만들 수 있어도 모든 종류의 생성 문제에서 가장 쉬운 선택은 아니다. 학습 안정성이 큰 과제다.

## 셀프 체크 퀴즈
1. GAN에서 생성자와 판별자는 각각 어떤 역할을 하는가?
2. GAN의 경쟁 구조가 생성 품질 향상에 도움이 되는 이유는 무엇인가?
3. 모드 붕괴는 GAN에서 어떤 문제를 뜻하는가?

## source
- Ian J. Goodfellow et al. / Generative Adversarial Nets / 2014
- Ian Goodfellow, Yoshua Bengio, Aaron Courville / Deep Learning / 2016
- Alec Radford, Luke Metz, Soumith Chintala / Unsupervised Representation Learning with Deep Convolutional Generative Adversarial Networks / 2016