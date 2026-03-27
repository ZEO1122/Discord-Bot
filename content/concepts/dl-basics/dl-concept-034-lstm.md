---
briefing_key: "dl-concept-034-lstm"
track: "dl-basics"
mode: "concept"
title: "LSTM"
one_line: "LSTM은 게이트와 셀 상태를 사용해 긴 시퀀스의 정보를 더 오래 유지하도록 설계된 순환신경망이다."
discussion_prompt: "기억을 지울지, 쓸지, 꺼낼지를 나누어 조절하는 구조가 왜 긴 문맥 처리에 유리할까?"
---

## 핵심 설명
- LSTM(Long Short-Term Memory)은 입력 게이트, 망각 게이트, 출력 게이트를 이용해 정보 흐름을 조절한다.
- 핵심은 셀 상태라는 비교적 안정적인 경로를 두어, 오래 유지할 정보와 버릴 정보를 구분한다는 점이다. 이 덕분에 기본 RNN보다 긴 의존관계를 다루기 쉽다.
- 번역, 음성 인식, 시계열 예측 등에서 오랫동안 중요한 기본 구조로 쓰였다.
- 구조가 더 복잡하고 계산량도 늘지만, 장기 기억을 다루는 능력 때문에 기본 RNN의 한계를 크게 보완했다.

## 직관
- 노트를 그냥 한 장만 들고 다니는 대신, 보관함과 필터가 있는 다이어리를 쓰는 것과 비슷하다.
- 중요한 메모는 남기고, 불필요한 메모는 지우고, 필요한 순간에만 꺼내 읽는 비서 시스템으로 생각할 수 있다.

## 헷갈리기 쉬운 점
- LSTM이 모든 긴 문맥 문제를 완벽히 해결하는 것은 아니다. 매우 긴 시퀀스나 병렬 계산 측면에서는 다른 구조가 더 유리할 수 있다.
- 게이트가 많다고 무조건 더 좋은 것은 아니다. 과제와 자원에 따라 더 단순한 GRU가 충분할 때도 있다.

## 셀프 체크 퀴즈
1. LSTM의 셀 상태는 기본 RNN의 은닉 상태와 어떤 차이를 가지는가?
2. 망각 게이트는 왜 중요한가?
3. LSTM이 기본 RNN보다 장기 의존관계를 더 잘 다룰 수 있는 이유는 무엇인가?

## source
- Sepp Hochreiter, Jürgen Schmidhuber / Long Short-Term Memory / 1997
- Ian Goodfellow, Yoshua Bengio, Aaron Courville / Deep Learning / 2016
- Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola / Dive into Deep Learning