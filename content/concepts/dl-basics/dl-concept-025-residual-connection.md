---
briefing_key: "dl-concept-025-residual-connection"
track: "dl-basics"
mode: "concept"
title: "잔차 연결"
one_line: "잔차 연결은 입력을 몇 개 층을 건너뛰어 더해 주어 깊은 네트워크의 학습을 쉽게 만드는 구조다."
discussion_prompt: "깊이를 늘리면 표현력이 커질 수 있는데도 실제 학습은 오히려 어려워지는 이유를 잔차 연결이 어떻게 완화할까?"
---

## 핵심 설명
- 잔차 연결은 어떤 블록의 입력을 그 블록의 출력에 직접 더해 주는 구조다. 그래서 블록은 전체 함수를 처음부터 배우기보다 변화량만 배우면 된다.
- 깊은 네트워크에서는 층을 더 쌓았는데도 최적화가 어려워 성능이 나빠지는 일이 생길 수 있다. 잔차 연결은 이런 문제를 줄이는 데 큰 역할을 했다.
- 입력이 그대로 흐를 수 있는 우회 경로가 생기면 기울기 전달도 쉬워진다. 그래서 매우 깊은 모델도 비교적 안정적으로 학습된다.
- 대표적인 예가 ResNet이며, 이후 많은 모델 구조에 잔차 아이디어가 널리 퍼졌다.

## 직관
- 새 내용을 덧붙이는 편집 작업처럼, 전체 문서를 다시 쓰기보다 기존 내용에서 무엇을 바꿀지만 적는 방식과 비슷하다.
- 계단 대신 완만한 경사로를 하나 더 놓아 이동을 쉽게 만드는 구조로 생각할 수 있다.

## 헷갈리기 쉬운 점
- 잔차 연결이 있다고 해서 모든 깊은 모델 문제가 자동으로 사라지는 것은 아니다. 그래도 최적화 난도를 크게 낮춘 중요한 구조다.
- 잔차 연결은 단순한 출력 복사가 아니다. 본래 변환 결과와 입력을 함께 사용해 학습을 돕는 방식이다.

## 셀프 체크 퀴즈
1. 잔차 연결에서 블록이 변화량을 배운다고 말하는 이유는 무엇인가?
2. 잔차 연결이 깊은 네트워크의 기울기 흐름에 어떤 도움을 주는가?
3. ResNet이 딥러닝 역사에서 중요한 이유는 무엇인가?

## source
- Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun / Deep Residual Learning for Image Recognition / 2016
- Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola / Dive into Deep Learning
- Stanford / CS231n Convolutional Neural Networks Notes