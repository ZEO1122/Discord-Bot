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
