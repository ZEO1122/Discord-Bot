from __future__ import annotations

from scripts.fetch_trend_sources import build_arxiv_url, parse_arxiv_feed
import pytest

from scripts.post_trend_brief import (
    TREND_CAUTION_MESSAGE,
    NoFreshTrendSourcesError,
    TrendBrief,
    build_embed,
    normalize_source_url,
    select_fresh_sources,
)


SAMPLE_FEED = """<?xml version='1.0' encoding='UTF-8'?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <title>  Sample NLP Paper  </title>
    <published>2026-03-26T12:00:00Z</published>
    <link rel="alternate" href="https://arxiv.org/abs/1234.5678v1"/>
  </entry>
</feed>
"""


def test_build_arxiv_url_uses_track_mapping() -> None:
    url = build_arxiv_url(track="nlp", max_results=5)
    assert "search_query=%28cat%3Acs.CL+OR+cat%3Acs.AI%29" in url
    assert "max_results=5" in url


def test_build_arxiv_url_supports_llm_query() -> None:
    url = build_arxiv_url(track="llm", max_results=4)
    assert "llm" in url
    assert "alignment" in url
    assert "max_results=4" in url


def test_build_arxiv_url_supports_detection_segmentation_query() -> None:
    url = build_arxiv_url(track="detection-segmentation", max_results=2)
    assert "detection" in url
    assert "segmentation" in url


def test_build_arxiv_url_supports_vision_language_query() -> None:
    url = build_arxiv_url(track="vision-language", max_results=2)
    assert "vision-language" in url or "vision%2Dlanguage" in url
    assert "image-text" in url or "image%2Dtext" in url


def test_build_arxiv_url_supports_refined_multimodal_query() -> None:
    url = build_arxiv_url(track="multimodal", max_results=3)
    assert "multimodal" in url
    assert "cat%3Acs.CV" in url
    assert "cat%3Acs.CL" in url


def test_parse_arxiv_feed_extracts_sources() -> None:
    sources = parse_arxiv_feed(SAMPLE_FEED)
    assert len(sources) == 1
    assert sources[0].title == "Sample NLP Paper"
    assert sources[0].url == "https://arxiv.org/abs/1234.5678v1"
    assert sources[0].published_at == "2026-03-26"
    assert sources[0].source_type == "paper"


def test_select_fresh_sources_filters_seen_urls_by_normalized_arxiv_id() -> None:
    fetched_sources = [
        {
            "title": "Seen Versioned Paper",
            "url": "https://arxiv.org/abs/1234.5678v2",
            "published_at": "2026-03-26",
            "source_type": "paper",
        },
        {
            "title": "Fresh Paper",
            "url": "https://arxiv.org/abs/9999.1111v1",
            "published_at": "2026-03-27",
            "source_type": "paper",
        },
    ]
    history = {
        "nlp": [
            {
                "url": "https://arxiv.org/abs/1234.5678v1",
            }
        ]
    }
    selected = select_fresh_sources(track="nlp", fetched_sources=fetched_sources, history=history, max_results=2)
    assert len(selected) == 1
    assert selected[0]["title"] == "Fresh Paper"


def test_normalize_source_url_strips_arxiv_version_suffix() -> None:
    assert normalize_source_url("https://arxiv.org/abs/1234.5678v3") == "https://arxiv.org/abs/1234.5678"


def test_select_fresh_sources_raises_no_fresh_error_when_all_seen() -> None:
    fetched_sources = [
        {
            "title": "Seen Paper",
            "url": "https://arxiv.org/abs/1234.5678v2",
            "published_at": "2026-03-26",
            "source_type": "paper",
        }
    ]
    history = {"nlp": [{"url": "https://arxiv.org/abs/1234.5678v1"}]}
    with pytest.raises(NoFreshTrendSourcesError):
        select_fresh_sources(track="nlp", fetched_sources=fetched_sources, history=history, max_results=1)


def test_build_embed_includes_hallucination_caution_field() -> None:
    brief = TrendBrief(
        title="최근 NLP 동향",
        one_line="LLM 추론 최적화 논문이 많이 올라오고 있다.",
        what_happened="최근 논문들이 모델 효율과 추론 안정성에 집중하고 있다.",
        why_it_matters="서비스 적용성과 비용 효율에 직접적인 영향을 준다.",
        discussion_prompt="추론 최적화와 모델 성능 중 무엇을 더 우선해야 할까?",
        sources=[
            {
                "title": "Sample NLP Paper",
                "url": "https://arxiv.org/abs/1234.5678v1",
            }
        ],
    )
    embed = build_embed(brief, track="nlp")
    caution_field = embed.fields[-1]
    assert caution_field.name == "주의"
    assert caution_field.value == TREND_CAUTION_MESSAGE
