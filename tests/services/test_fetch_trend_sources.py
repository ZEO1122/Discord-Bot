from __future__ import annotations

from scripts.fetch_trend_sources import build_arxiv_url, parse_arxiv_feed
from scripts.post_trend_brief import normalize_source_url, select_fresh_sources


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
