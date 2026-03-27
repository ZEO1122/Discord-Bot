from __future__ import annotations

from pathlib import Path

from scripts.post_concept_brief import parse_brief


def test_parse_brief_supports_generated_concept_format(tmp_path: Path) -> None:
    brief_path = tmp_path / "generated.md"
    brief_path.write_text(
        """---
briefing_key: generated-001
track: dl-basics
mode: concept
title: 퍼셉트론
one_line: 퍼셉트론은 가장 기본적인 이진 분류 모델이다.
discussion_prompt: 왜 아직도 퍼셉트론을 배우는가?
---

## 핵심 설명
- 퍼셉트론은 입력의 가중합을 기준으로 출력을 결정한다.

## 직관
- 총점이 기준 이상이면 통과라고 판단하는 방식과 비슷하다.

## 헷갈리기 쉬운 점
- 단일 퍼셉트론은 모든 문제를 풀 수 없다.

## source
- Rosenblatt / The Perceptron / 1958
""",
        encoding="utf-8",
    )

    brief = parse_brief(brief_path)

    assert brief.briefing_key == "generated-001"
    assert brief.what_happened.startswith("- 퍼셉트론")
    assert "총점이 기준 이상" in brief.why_it_matters
    assert brief.sources[0]["title"] == "Rosenblatt / The Perceptron / 1958"


def test_parse_brief_supports_current_concept_heading_variants(tmp_path: Path) -> None:
    brief_path = tmp_path / "current-format.md"
    brief_path.write_text(
        """---
briefing_key: generated-002
track: dl-basics
mode: concept
title: 순전파
one_line: 순전파는 입력이 예측값으로 변환되는 계산 과정이다.
discussion_prompt: 왜 순전파를 먼저 이해해야 할까?
---

## 오늘의 개념
- 순전파는 입력이 네트워크를 통과하는 계산 과정이다.

## 핵심 요약
- 입력이 층을 거치며 예측값으로 바뀐다.

## 왜 중요한가
- 손실 함수는 순전파 결과를 바탕으로 계산된다.

## 용어 빠르게 이해하기
- 활성값: 층 사이에서 전달되는 중간 출력

## source
- Deep Learning / 2016
""",
        encoding="utf-8",
    )

    brief = parse_brief(brief_path)

    assert brief.briefing_key == "generated-002"
    assert "예측값" in brief.what_happened
    assert "손실 함수" in brief.why_it_matters
    assert brief.easy_terms == ["활성값: 층 사이에서 전달되는 중간 출력"]
    assert brief.sources[0]["title"] == "Deep Learning / 2016"
