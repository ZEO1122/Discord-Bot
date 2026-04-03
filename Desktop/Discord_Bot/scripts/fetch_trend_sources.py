from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
import re
import time
from typing import Final
from urllib import error, parse, request
import xml.etree.ElementTree as ET


ARXIV_API_URL: Final[str] = "https://export.arxiv.org/api/query"
ATOM_NS: Final[dict[str, str]] = {"atom": "http://www.w3.org/2005/Atom"}
ARXIV_NS: Final[dict[str, str]] = {"arxiv": "http://arxiv.org/schemas/atom"}
TRACK_QUERY_MAP: Final[dict[str, str]] = {
    "nlp": "(cat:cs.CL OR cat:cs.AI) AND (all:language OR all:llm OR all:translation OR all:reasoning)",
    "cv": "cat:cs.CV AND (all:vision OR all:detection OR all:segmentation OR all:diffusion)",
    "multimodal": "(cat:cs.CV OR cat:cs.CL OR cat:cs.AI) AND (all:multimodal OR all:vision-language OR all:text-image OR all:video-language)",
    "dl-basics": "cat:cs.LG",
}


SourceRecord = dict[str, object]


@dataclass(slots=True)
class TrendSource:
    title: str
    url: str
    published_at: str
    source_type: str
    abstract: str
    authors: list[str]
    doi: str
    arxiv_id: str


def normalize_arxiv_id(value: str) -> str:
    normalized = value.strip()
    if not normalized:
        return ""
    if "/abs/" in normalized:
        normalized = normalized.split("/abs/", 1)[1]
    normalized = normalized.split("?", 1)[0].split("/", 1)[0]
    return re.sub(r"v\d+$", "", normalized)


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
        abstract = (entry.findtext("atom:summary", default="", namespaces=ATOM_NS) or "").strip()
        published_raw = (entry.findtext("atom:published", default="", namespaces=ATOM_NS) or "").strip()
        doi = (entry.findtext("arxiv:doi", default="", namespaces=ARXIV_NS) or "").strip()
        authors = [
            (author.findtext("atom:name", default="", namespaces=ATOM_NS) or "").strip()
            for author in entry.findall("atom:author", ATOM_NS)
        ]
        html_url = ""
        for link in entry.findall("atom:link", ATOM_NS):
            if link.attrib.get("rel") == "alternate":
                html_url = link.attrib.get("href", "")
                break

        if not title or not html_url:
            continue

        published_at = published_raw[:10] if published_raw else datetime.now(UTC).date().isoformat()
        arxiv_id = normalize_arxiv_id(html_url)
        sources.append(
            TrendSource(
                title=title.replace("\n", " ").strip(),
                url=html_url,
                published_at=published_at,
                source_type="paper",
                abstract=abstract.replace("\n", " ").strip(),
                authors=[author for author in authors if author],
                doi=doi,
                arxiv_id=arxiv_id,
            )
        )
    return sources


def fetch_trend_sources(track: str, max_results: int = 5) -> list[SourceRecord]:
    api_url = build_arxiv_url(track, max_results)
    http_request = request.Request(
        api_url,
        headers={
            "User-Agent": "Discord-Bot/1.0 (GitHub Actions trend fetch)",
        },
    )
    xml_text = ""
    for attempt in range(1, 4):
        try:
            with request.urlopen(http_request, timeout=60) as response:
                xml_text = response.read().decode("utf-8")
                break
        except error.HTTPError as exc:
            if exc.code == 429 and attempt < 4:
                retry_after = exc.headers.get("Retry-After")
                delay = int(retry_after) if retry_after and retry_after.isdigit() else attempt * 10
                time.sleep(delay)
                continue
            if exc.code == 429:
                raise RuntimeError("Trend source fetch was rate-limited by arXiv after retries.") from exc
            raise RuntimeError(f"Trend source fetch failed with HTTP {exc.code}.") from exc
    if not xml_text:
        raise RuntimeError(f"Trend source fetch failed for track={track}")

    sources = parse_arxiv_feed(xml_text)
    if not sources:
        raise RuntimeError(f"No trend sources fetched for track={track}")
    return [
        {
            "title": source.title,
            "url": source.url,
            "published_at": source.published_at,
            "source_type": source.source_type,
            "abstract": source.abstract,
            "authors": source.authors,
            "doi": source.doi,
            "arxiv_id": source.arxiv_id,
        }
        for source in sources
    ]
