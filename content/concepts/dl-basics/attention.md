---
briefing_key: dl-basics-attention-001
track: dl-basics
mode: concept
title: 어텐션은 왜 중요한가
one_line: 어텐션은 입력 전체 중 중요한 부분에 더 집중하도록 돕는 메커니즘이다.
discussion_prompt: Transformer가 RNN보다 유리한 상황은 언제일까?
sources:
  - title: Attention Is All You Need
    url: https://arxiv.org/abs/1706.03762
    source_type: paper
---

## 무슨 내용인가
어텐션은 입력 전체를 한 번에 참고하면서 현재 출력에 중요한 위치에 더 큰 가중치를 주는 방식이다.
이 방식은 긴 문장에서 멀리 떨어진 정보도 직접 연결할 수 있게 해준다.
Transformer 계열 모델은 이 아이디어를 중심으로 설계되었다.

## 왜 중요한가
어텐션 덕분에 긴 문장, 긴 문서, 멀티모달 입력에서도 중요한 정보에 더 잘 집중할 수 있다.
번역, 요약, 질의응답, 이미지-텍스트 모델까지 다양한 현대 AI 모델의 핵심 기반이 된다.

## 쉬운 용어
- Attention: 중요한 정보에 더 집중하도록 하는 메커니즘
- Token: 모델이 처리하는 텍스트 조각
- Weight: 각 정보가 얼마나 중요한지 나타내는 값
