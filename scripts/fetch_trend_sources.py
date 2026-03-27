from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Final
from urllib import error, parse, request
import xml.etree.ElementTree as ET


ARXIV_API_URL: Final[str] = "http://export.arxiv.org/api/query"
ATOM_NS: Final[dict[str, str]] = {"atom": "http://www.w3.org/2005/Atom"}
TRACK_QUERY_MAP: Final[dict[str, str]] = {
    "nlp": "cat:cs.CL",
    "cv": "cat:cs.CV",
    "multimodal": "all:multimodal AND (cat:cs.CV OR cat:cs.CL OR cat:cs.AI)",
    "dl-basics": "cat:cs.LG",
}


@dataclass(slots=True)
class TrendSource:
    title: str
    url: str
    published_at: str
    source_type: str


def build_arxiv_url(track: str, max_results: int) -> str:
    query = TRACK_QUERY_MAP.get(track, f"all:{track}")
    params = {
        "search_query": query,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
        "start": 0,
        "max_results": max_results,
    }
    return f"{ARXIV_API_URL}?{parse.urlencode(params)}"


def parse_arxiv_feed(xml_text: str) -> list[TrendSource]:
    root = ET.fromstring(xml_text)
    sources: list[TrendSource] = []
    for entry in root.findall("atom:entry", ATOM_NS):
        title = (entry.findtext("atom:title", default="", namespaces=ATOM_NS) or "").strip()
        published_raw = (entry.findtext("atom:published", default="", namespaces=ATOM_NS) or "").strip()
        html_url = ""
        for link in entry.findall("atom:link", ATOM_NS):
            if link.attrib.get("rel") == "alternate":
                html_url = link.attrib.get("href", "")
                break

        if not title or not html_url:
            continue

        published_at = published_raw[:10] if published_raw else datetime.now(UTC).date().isoformat()
        sources.append(
            TrendSource(
                title=title.replace("\n", " ").strip(),
                url=html_url,
                published_at=published_at,
                source_type="paper",
            )
        )
    return sources


def fetch_trend_sources(track: str, max_results: int = 5) -> list[dict[str, str]]:
    api_url = build_arxiv_url(track, max_results)
    http_request = request.Request(
        api_url,
        headers={
            "User-Agent": "Discord-Bot/1.0 (GitHub Actions trend fetch)",
        },
    )
    try:
        with request.urlopen(http_request, timeout=60) as response:
            xml_text = response.read().decode("utf-8")
    except error.HTTPError as exc:
        if exc.code == 429:
            raise RuntimeError("Trend source fetch was rate-limited by arXiv. Retry later.") from exc
        raise RuntimeError(f"Trend source fetch failed with HTTP {exc.code}.") from exc

    sources = parse_arxiv_feed(xml_text)
    if not sources:
        raise RuntimeError(f"No trend sources fetched for track={track}")
    return [
        {
            "title": source.title,
            "url": source.url,
            "published_at": source.published_at,
            "source_type": source.source_type,
        }
        for source in sources
    ]
