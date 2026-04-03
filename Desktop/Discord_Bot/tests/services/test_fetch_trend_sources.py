from __future__ import annotations

from scripts.fetch_trend_sources import build_arxiv_url, parse_arxiv_feed
import pytest

from scripts.post_trend_brief import (
    TREND_CAUTION_MESSAGE,
    NoFreshTrendSourcesError,
    TrendBrief,
    build_fetch_count,
    build_embed,
    build_selection_breakdown,
    extract_arxiv_id,
    format_selection_log_line,
    normalize_source_url,
    select_fresh_sources,
)


SAMPLE_FEED = """<?xml version='1.0' encoding='UTF-8'?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:arxiv="http://arxiv.org/schemas/atom">
  <entry>
    <title>  Sample NLP Paper  </title>
    <published>2026-03-26T12:00:00Z</published>
    <summary>Transformer reasoning for language tasks.</summary>
    <author><name>Jane Researcher</name></author>
    <author><name>John Scientist</name></author>
    <arxiv:doi>10.48550/arXiv.1234.5678</arxiv:doi>
    <link rel="alternate" href="https://arxiv.org/abs/1234.5678v1"/>
  </entry>
</feed>
"""


def test_build_arxiv_url_uses_track_mapping() -> None:
    url = build_arxiv_url(track="nlp", max_results=5)
    assert "search_query=%28cat%3Acs.CL+OR+cat%3Acs.AI%29" in url
    assert "max_results=5" in url


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
    assert sources[0].abstract == "Transformer reasoning for language tasks."
    assert sources[0].authors == ["Jane Researcher", "John Scientist"]
    assert sources[0].doi == "10.48550/arXiv.1234.5678"
    assert sources[0].arxiv_id == "1234.5678"


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
            "abstract": "A language reasoning paper.",
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
    assert "selection_score" in selected[0]


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


def test_select_fresh_sources_ranks_non_retracted_candidates(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "scripts.post_trend_brief.fetch_openalex_metadata",
        lambda arxiv_id, title, published_at: {
            "Top paper": {
                "openalex_matched": True,
                "openalex_cited_by_count": 42,
                "openalex_fwci": 12.0,
                "openalex_citation_percentile": 0.95,
                "openalex_is_retracted": False,
                "openalex_has_fulltext": True,
                "openalex_is_oa": True,
            },
            "Retracted paper": {
                "openalex_matched": True,
                "openalex_is_retracted": True,
            },
        }.get(title, {}),
    )
    monkeypatch.setattr(
        "scripts.post_trend_brief.fetch_huggingface_metadata",
        lambda arxiv_id: {"hf_upvotes": 80, "hf_github_stars": 1200, "hf_daily_rank": 2},
    )
    fetched_sources = [
        {
            "title": "Retracted paper",
            "url": "https://arxiv.org/abs/1111.1111v1",
            "published_at": "2026-03-27",
            "source_type": "paper",
            "abstract": "language model",
            "arxiv_id": "1111.1111",
        },
        {
            "title": "Top paper",
            "url": "https://arxiv.org/abs/2222.2222v1",
            "published_at": "2026-03-26",
            "source_type": "paper",
            "abstract": "language model reasoning transformer",
            "arxiv_id": "2222.2222",
        },
    ]

    selected = select_fresh_sources(track="nlp", fetched_sources=fetched_sources, history={}, max_results=2)

    assert [item["title"] for item in selected] == ["Top paper"]
    selection_score = selected[0]["selection_score"]
    assert isinstance(selection_score, float)
    assert selection_score > 0


def test_selection_helpers_cover_breakdown_and_logging() -> None:
    source = {
        "title": "Reasoning Transformer",
        "url": "https://arxiv.org/abs/9999.1111v2",
        "published_at": "2026-03-27",
        "abstract": "A transformer for language reasoning.",
        "doi": "10.48550/arXiv.9999.1111",
        "openalex_matched": True,
        "openalex_cited_by_count": 24,
        "openalex_fwci": 8.5,
        "openalex_citation_percentile": 0.8,
        "openalex_has_fulltext": True,
        "openalex_is_oa": True,
        "hf_upvotes": 50,
        "hf_github_stars": 4000,
        "hf_daily_rank": 3,
        "selection_score": 12.3,
    }
    breakdown = build_selection_breakdown("nlp", source)
    assert breakdown["track_relevance"] > 4
    assert breakdown["community"] > 0
    assert extract_arxiv_id(source["url"]) == "9999.1111"
    assert "selection track=nlp" in format_selection_log_line("nlp", source | {"selection_breakdown": breakdown})


def test_build_fetch_count_expands_candidate_pool() -> None:
    assert build_fetch_count(3) == 12
    assert build_fetch_count(10) == 20


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
