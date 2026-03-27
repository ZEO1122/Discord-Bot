from __future__ import annotations

from scripts.fetch_trend_sources import build_arxiv_url, parse_arxiv_feed


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
    assert "search_query=cat%3Acs.CL" in url
    assert "max_results=5" in url


def test_parse_arxiv_feed_extracts_sources() -> None:
    sources = parse_arxiv_feed(SAMPLE_FEED)
    assert len(sources) == 1
    assert sources[0].title == "Sample NLP Paper"
    assert sources[0].url == "https://arxiv.org/abs/1234.5678v1"
    assert sources[0].published_at == "2026-03-26"
    assert sources[0].source_type == "paper"
