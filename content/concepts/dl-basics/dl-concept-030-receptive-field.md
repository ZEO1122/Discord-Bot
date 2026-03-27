---
briefing_key: "dl-concept-030-receptive-field"
track: "dl-basics"
mode: "concept"
title: "수용영역"
one_line: "수용영역은 특정 뉴런의 출력에 영향을 주는 입력 영역의 범위를 뜻한다."
discussion_prompt: "깊은 층으로 갈수록 더 넓은 문맥을 볼 수 있다는 말을 수용영역으로 어떻게 설명할 수 있을까?"
---

## 핵심 설명
- 수용영역은 특징 맵의 한 위치가 원래 입력의 어느 범위를 참고해 계산되었는지를 나타낸다.
- 초기 층의 뉴런은 작은 지역만 보지만, 층이 깊어질수록 여러 지역 특징이 합쳐져 더 넓은 입력 범위를 보게 된다.
- 수용영역이 충분히 크지 않으면 모델은 전체 물체나 긴 문맥을 파악하기 어렵다. 반대로 너무 빠르게 커지면 세밀한 정보가 약해질 수 있다.
- 커널 크기, 스트라이드, 풀링, 네트워크 깊이는 모두 수용영역의 크기와 성장 방식에 영향을 준다.

## 직관
- 돋보기로 아주 작은 부분만 보면 점 하나만 보이고, 점점 멀리서 보면 모양 전체가 보이는 것과 비슷하다.
- 한 사람이 주변 두세 명의 말만 들을 때와, 여러 단계를 거쳐 회의 전체 맥락을 듣는 상황의 차이로 이해할 수 있다.

## 헷갈리기 쉬운 점
- 특징 맵의 해상도가 작다고 해서 항상 수용영역이 충분히 크다는 뜻은 아니다. 어떤 연산을 거쳤는지가 중요하다.
- 이론적 수용영역과 실제로 강하게 활용되는 영역은 다를 수 있다. 개념적으로는 입력 영향 범위를 보는 도구다.

## 셀프 체크 퀴즈
1. 수용영역은 무엇을 설명하는 개념인가?
2. 깊은 층으로 갈수록 수용영역이 커지는 이유는 무엇인가?
3. 수용영역이 너무 작으면 어떤 종류의 정보를 놓치기 쉬운가?

## source
- Vincent Dumoulin, Francesco Visin / A Guide to Convolution Arithmetic for Deep Learning / 2016
- Ian Goodfellow, Yoshua Bengio, Aaron Courville / Deep Learning / 2016
- Stanford / CS231n Convolutional Neural Networks Notes