---
briefing_key: "dl-concept-036-attention"
track: "dl-basics"
mode: "concept"
title: "어텐션"
one_line: "어텐션은 모델이 입력 전체를 똑같이 보지 않고 현재 필요한 부분에 더 큰 가중치를 두게 하는 메커니즘이다."
discussion_prompt: "모든 정보를 같은 비중으로 처리하지 않고 중요한 부분만 더 주목하는 전략이 왜 효과적일까?"
---

## 핵심 설명
- 어텐션은 현재 작업에 관련 있는 입력이나 은닉 상태에 더 큰 가중치를 부여해 정보를 읽는 방식이다.
- 이 메커니즘 덕분에 모델은 고정 길이 벡터 하나에 모든 정보를 억지로 압축하지 않고, 필요할 때 필요한 부분을 다시 참조할 수 있다.
- 기계 번역에서는 현재 생성 중인 단어와 관련된 입력 위치를 더 강하게 볼 수 있어 성능 향상에 큰 기여를 했다.
- 어텐션은 이후 셀프 어텐션과 트랜스포머로 확장되며 현대 딥러닝의 핵심 아이디어가 되었다.

## 직관
- 긴 문서를 읽을 때 모든 문장을 같은 비중으로 기억하지 않고, 현재 질문과 관련된 부분만 다시 찾아보는 것과 비슷하다.
- 발표를 들으며 지금 말하는 주제와 직접 연결된 슬라이드에 눈이 더 가는 상황으로 생각할 수 있다.

## 헷갈리기 쉬운 점
- 어텐션은 단순한 중요도 표시가 아니다. 가중치를 이용해 실제로 어떤 정보를 얼마나 섞어 읽을지를 결정한다.
- 어텐션이 있다고 해서 문맥을 완벽히 이해하는 것은 아니다. 그래도 관련 부분을 선택적으로 참고하게 만든다는 점이 핵심이다.

## 셀프 체크 퀴즈
1. 어텐션이 고정 길이 압축의 한계를 완화하는 이유는 무엇인가?
2. 기계 번역에서 어텐션이 특히 유용한 이유는 무엇인가?
3. 어텐션 가중치는 모델의 어떤 행동을 바꾸는가?

## source
- Dzmitry Bahdanau, Kyunghyun Cho, Yoshua Bengio / Neural Machine Translation by Jointly Learning to Align and Translate / 2015
- Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola / Dive into Deep Learning
- Stanford / CS224n Attention Notes