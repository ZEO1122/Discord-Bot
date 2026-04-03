from __future__ import annotations

# pyright: reportMissingImports=false

import argparse
from dataclasses import dataclass
from datetime import UTC, date, datetime
from functools import lru_cache
import json
from pathlib import Path
import re
import sys
from typing import Mapping, Sequence
from urllib import parse, request

import requests

import discord

try:
    from scripts.fetch_trend_sources import fetch_trend_sources
except ImportError:
    from fetch_trend_sources import fetch_trend_sources


TREND_CAUTION_MESSAGE = (
    "주의: 이 브리핑은 최신 source를 바탕으로 GPT가 요약한 내용입니다. "
    "해석 오류나 누락 가능성이 있으니 원문 출처를 함께 확인하세요."
)
OPENALEX_API_BASE = "https://api.openalex.org"
HUGGINGFACE_PAPERS_BASE = "https://huggingface.co/papers"
HTTP_TIMEOUT_SECONDS = 20
TRACK_KEYWORDS: dict[str, tuple[str, ...]] = {
    "nlp": ("language", "llm", "translation", "reasoning", "retrieval", "transformer"),
    "cv": ("vision", "image", "video", "detection", "segmentation", "diffusion"),
    "multimodal": ("multimodal", "vision-language", "text-image", "video-language", "audio", "cross-modal"),
    "dl-basics": ("neural", "representation", "training", "optimization", "transformer", "learning"),
}
SourceRecord = dict[str, object]


class NoFreshTrendSourcesError(RuntimeError):
    pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate and post a trend brief to Discord.")
    parser.add_argument("--track", required=True)
    parser.add_argument("--max-results", type=int, default=5)
    parser.add_argument("--history-file", default="content/trends/history/published_trends.json")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def bootstrap_pythonpath() -> None:
    root = Path(__file__).resolve().parents[1]
    src = root / "src"
    if str(src) not in sys.path:
        sys.path.insert(0, str(src))


@dataclass(slots=True)
class TrendBrief:
    title: str
    one_line: str
    what_happened: str
    why_it_matters: str
    discussion_prompt: str
    sources: list[SourceRecord]


def build_fetch_count(max_results: int) -> int:
    return min(max(max_results * 4, max_results + 5), 20)


def normalize_source_url(url: str) -> str:
    normalized = url.strip()
    if "arxiv.org/abs/" in normalized:
        prefix, arxiv_id = normalized.split("/abs/", 1)
        arxiv_id = arxiv_id.split("?", 1)[0]
        if "v" in arxiv_id and arxiv_id.rsplit("v", 1)[-1].isdigit():
            arxiv_id = arxiv_id.rsplit("v", 1)[0]
        return f"{prefix}/abs/{arxiv_id}"
    return normalized


def extract_arxiv_id(url: str) -> str:
    normalized = normalize_source_url(url)
    if "/abs/" not in normalized:
        return ""
    return normalized.split("/abs/", 1)[1].split("/", 1)[0]


def normalize_title(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", value.lower())).strip()


def parse_published_date(value: str) -> date | None:
    try:
        return datetime.strptime(value[:10], "%Y-%m-%d").date()
    except ValueError:
        return None


def as_float(value: object, default: float = 0.0) -> float:
    if isinstance(value, bool):
        return float(default)
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return default
    return default


def as_int(value: object, default: int = 0) -> int:
    if isinstance(value, bool):
        return default
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            return default
    return default


def score_recency(published_at: str, *, today: date | None = None) -> float:
    published_date = parse_published_date(published_at)
    if published_date is None:
        return 0.0
    current_day = today or datetime.now(UTC).date()
    age_days = max((current_day - published_date).days, 0)
    if age_days <= 7:
        return 30.0
    if age_days >= 45:
        return 0.0
    return round(30.0 * (45 - age_days) / 38, 2)


def score_track_relevance(track: str, source: Mapping[str, object]) -> float:
    keywords = TRACK_KEYWORDS.get(track, ())
    if not keywords:
        return 8.0
    haystack = f"{source.get('title', '')} {source.get('abstract', '')}".lower()
    matches = sum(1 for keyword in keywords if keyword in haystack)
    if matches == 0:
        return 4.0
    return round(min(15.0, 4.0 + (11.0 * matches / len(keywords))), 2)


def score_openalex_impact(source: Mapping[str, object]) -> float:
    percentile_value = as_float(source.get("openalex_citation_percentile", 0.0))
    fwci = as_float(source.get("openalex_fwci", 0.0))
    cited_by_count = as_int(source.get("openalex_cited_by_count", 0))
    percentile_score = min(12.0, percentile_value * 12.0)
    fwci_score = min(5.0, fwci / 20.0 * 5.0)
    citation_score = min(3.0, cited_by_count / 100.0 * 3.0)
    return round(percentile_score + fwci_score + citation_score, 2)


def score_citation_velocity(source: Mapping[str, object]) -> float:
    cited_by_count = as_int(source.get("openalex_cited_by_count", 0))
    published_at = str(source.get("published_at", ""))
    published_date = parse_published_date(published_at)
    if published_date is None:
        return 0.0
    age_days = max((datetime.now(UTC).date() - published_date).days, 0)
    months_since_publish = max(age_days / 30.0, 1.0)
    citations_per_month = cited_by_count / months_since_publish
    return round(min(10.0, citations_per_month), 2)


def score_reliability(source: Mapping[str, object]) -> float:
    if source.get("openalex_is_retracted"):
        return 0.0
    score = 4.0
    if source.get("doi") or source.get("openalex_doi"):
        score += 2.0
    if source.get("openalex_has_fulltext"):
        score += 2.0
    if source.get("openalex_is_oa"):
        score += 1.0
    if source.get("openalex_matched"):
        score += 1.0
    return round(min(10.0, score), 2)


def score_community_signal(source: Mapping[str, object]) -> float:
    upvotes = as_int(source.get("hf_upvotes", 0))
    github_stars = as_int(source.get("hf_github_stars", 0))
    daily_rank = as_int(source.get("hf_daily_rank", 0))
    upvote_score = min(5.0, upvotes / 150.0 * 5.0)
    github_score = min(7.0, github_stars / 50000.0 * 7.0)
    daily_rank_score = 0.0
    if daily_rank == 1:
        daily_rank_score = 3.0
    elif 1 < daily_rank <= 5:
        daily_rank_score = 2.0
    elif 5 < daily_rank <= 10:
        daily_rank_score = 1.0
    return round(upvote_score + github_score + daily_rank_score, 2)


def build_selection_breakdown(track: str, source: Mapping[str, object]) -> dict[str, float]:
    return {
        "recency": score_recency(str(source.get("published_at", ""))),
        "impact": score_openalex_impact(source),
        "velocity": score_citation_velocity(source),
        "reliability": score_reliability(source),
        "track_relevance": score_track_relevance(track, source),
        "community": score_community_signal(source),
    }


@lru_cache(maxsize=256)
def fetch_openalex_metadata(arxiv_id: str, title: str, published_at: str) -> dict[str, object]:
    headers = {"User-Agent": "Discord-Bot/1.0 (trend ranking)"}
    if arxiv_id:
        doi_url = parse.quote(f"https://doi.org/10.48550/arXiv.{arxiv_id}", safe="")
        try:
            response = requests.get(
                f"{OPENALEX_API_BASE}/works/{doi_url}",
                headers=headers,
                timeout=HTTP_TIMEOUT_SECONDS,
            )
            if response.status_code == 200:
                return parse_openalex_work(response.json())
        except requests.RequestException:
            pass

    try:
        response = requests.get(
            f"{OPENALEX_API_BASE}/works",
            params={"search": title, "per-page": 5},
            headers=headers,
            timeout=HTTP_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
    except requests.RequestException:
        return {}

    payload = response.json()
    raw_results = payload.get("results", []) if isinstance(payload, dict) else []
    results = raw_results if isinstance(raw_results, list) else []
    candidate = choose_openalex_candidate(
        results=[item for item in results if isinstance(item, dict)],
        arxiv_id=arxiv_id,
        title=title,
        published_at=published_at,
    )
    return parse_openalex_work(candidate) if candidate else {}


def choose_openalex_candidate(
    *,
    results: list[SourceRecord],
    arxiv_id: str,
    title: str,
    published_at: str,
) -> SourceRecord | None:
    target_title = normalize_title(title)
    parsed_date = parse_published_date(published_at)
    target_year = parsed_date.year if parsed_date else None
    best_match: tuple[float, SourceRecord] | None = None
    for item in results:
        score = 0.0
        item_title = normalize_title(str(item.get("display_name", "")))
        ids = item.get("ids") or {}
        ids_doi = str(ids.get("doi", "")) if isinstance(ids, dict) else ""
        if arxiv_id and arxiv_id.lower() in ids_doi.lower():
            score += 5.0
        if item_title == target_title:
            score += 4.0
        elif target_title and (item_title.startswith(target_title) or target_title.startswith(item_title)):
            score += 2.0
        publication_year = item.get("publication_year")
        if target_year and isinstance(publication_year, int):
            year_delta = abs(publication_year - target_year)
            if year_delta == 0:
                score += 2.0
            elif year_delta == 1:
                score += 1.0
        if best_match is None or score > best_match[0]:
            best_match = (score, item)
    if best_match is None or best_match[0] < 4.0:
        return None
    return best_match[1]


def parse_openalex_work(item: Mapping[str, object]) -> dict[str, object]:
    open_access_raw = item.get("open_access")
    open_access = open_access_raw if isinstance(open_access_raw, dict) else {}
    citation_percentile_raw = item.get("citation_normalized_percentile")
    citation_percentile = citation_percentile_raw if isinstance(citation_percentile_raw, dict) else {}
    ids_raw = item.get("ids")
    ids = ids_raw if isinstance(ids_raw, dict) else {}
    primary_topic_raw = item.get("primary_topic")
    primary_topic = primary_topic_raw if isinstance(primary_topic_raw, dict) else {}
    return {
        "openalex_matched": True,
        "openalex_cited_by_count": as_int(item.get("cited_by_count", 0)),
        "openalex_fwci": as_float(item.get("fwci", 0.0)),
        "openalex_citation_percentile": as_float(citation_percentile.get("value", 0.0)),
        "openalex_is_retracted": bool(item.get("is_retracted", False)),
        "openalex_has_fulltext": bool(open_access.get("any_repository_has_fulltext", False)),
        "openalex_is_oa": bool(open_access.get("is_oa", False)),
        "openalex_doi": str(ids.get("doi", "")),
        "openalex_topic": str(primary_topic.get("display_name", "")),
    }


@lru_cache(maxsize=256)
def fetch_huggingface_metadata(arxiv_id: str) -> dict[str, object]:
    if not arxiv_id:
        return {}
    try:
        response = requests.get(
            f"{HUGGINGFACE_PAPERS_BASE}/{arxiv_id}",
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=HTTP_TIMEOUT_SECONDS,
        )
        if response.status_code != 200:
            return {}
    except requests.RequestException:
        return {}

    text = response.text
    github_match = re.search(r'githubStars&quot;:(\d+)', text)
    rank_match = re.search(r'dailyPaperRank&quot;:(\d+)', text)
    upvote_match = re.search(r'Upvote[^0-9]{0,20}(\d+)', text, re.IGNORECASE)
    return {
        "hf_github_stars": int(github_match.group(1)) if github_match else 0,
        "hf_daily_rank": int(rank_match.group(1)) if rank_match else 0,
        "hf_upvotes": int(upvote_match.group(1)) if upvote_match else 0,
    }


def enrich_source_for_selection(track: str, source: Mapping[str, object]) -> SourceRecord:
    enriched = dict(source)
    arxiv_id = str(enriched.get("arxiv_id", "") or extract_arxiv_id(str(enriched.get("url", ""))))
    if arxiv_id:
        enriched["arxiv_id"] = arxiv_id

    openalex_metadata = fetch_openalex_metadata(arxiv_id, str(enriched.get("title", "")), str(enriched.get("published_at", "")))
    huggingface_metadata = fetch_huggingface_metadata(arxiv_id)
    enriched.update(openalex_metadata)
    enriched.update(huggingface_metadata)

    breakdown = build_selection_breakdown(track, enriched)
    enriched["selection_breakdown"] = breakdown
    enriched["selection_score"] = round(sum(breakdown.values()), 2)
    return enriched


def rank_trend_sources(track: str, fresh_sources: Sequence[Mapping[str, object]]) -> list[SourceRecord]:
    ranked_sources: list[SourceRecord] = []
    for source in fresh_sources:
        enriched = enrich_source_for_selection(track, source)
        if enriched.get("openalex_is_retracted"):
            continue
        ranked_sources.append(enriched)
    ranked_sources.sort(
        key=lambda item: (
            as_float(item.get("selection_score", 0.0)),
            str(item.get("published_at", "")),
            str(item.get("title", "")),
        ),
        reverse=True,
    )
    return ranked_sources


def format_selection_log_line(track: str, source: Mapping[str, object]) -> str:
    breakdown = source.get("selection_breakdown", {})
    if not isinstance(breakdown, dict):
        breakdown = {}
    breakdown_text = ",".join(f"{key}={value}" for key, value in sorted(breakdown.items()))
    return (
        f"selection track={track} score={source.get('selection_score', 0)} "
        f"title={source.get('title', '')} breakdown={breakdown_text}"
    )


def load_history(history_path: Path) -> dict[str, list[dict[str, str]]]:
    if not history_path.exists():
        return {}
    return json.loads(history_path.read_text(encoding="utf-8"))


def select_fresh_sources(
    track: str,
    fetched_sources: Sequence[Mapping[str, object]],
    history: dict[str, list[dict[str, str]]],
    max_results: int,
) -> list[SourceRecord]:
    seen_urls = {normalize_source_url(item["url"]) for item in history.get(track, [])}
    fresh_sources = [source for source in fetched_sources if normalize_source_url(str(source["url"])) not in seen_urls]
    if not fresh_sources:
        raise NoFreshTrendSourcesError(f"No fresh trend sources available for track={track}")
    ranked_sources = rank_trend_sources(track, fresh_sources)
    if not ranked_sources:
        raise NoFreshTrendSourcesError(f"No rankable trend sources available for track={track}")
    return ranked_sources[:max_results]


def update_history(
    history_path: Path,
    track: str,
    generated_title: str,
    selected_sources: Sequence[Mapping[str, object]],
) -> None:
    history = load_history(history_path)
    track_history = history.get(track, [])
    posted_at = datetime.now(UTC).isoformat()
    for source in selected_sources:
        track_history.append(
            {
                "title": generated_title,
                "source_title": str(source["title"]),
                "url": normalize_source_url(str(source["url"])),
                "published_at": str(source.get("published_at", "")),
                "posted_at": posted_at,
            }
        )
    history[track] = track_history[-50:]
    history_path.parent.mkdir(parents=True, exist_ok=True)
    history_path.write_text(json.dumps(history, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_prompt(track: str, sources: Sequence[Mapping[str, object]]) -> str:
    source_lines = "\n".join(
        f"- {str(item['title'])} | {str(item['url'])} | {str(item.get('published_at', ''))}" for item in sources
    )
    return (
        "당신은 AI 학술동아리용 브리핑 에디터다.\n"
        f"트랙: {track}\n"
        "아래 출처만 근거로 한국어 브리핑을 작성하라.\n"
        "반드시 JSON으로만 답하라.\n"
        "필수 키: title, one_line, what_happened, why_it_matters, discussion_prompt\n"
        "출처를 바꾸거나 추가하지 마라.\n\n"
        f"출처 목록:\n{source_lines}\n"
    )


def generate_with_openai(prompt: str, api_key: str) -> dict[str, str]:
    model = __import__("os").getenv("OPENAI_MODEL", "gpt-5.1")
    payload = {
        "model": model,
        "input": prompt,
        "text": {"format": {"type": "json_object"}},
    }
    req = request.Request(
        "https://api.openai.com/v1/responses",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with request.urlopen(req, timeout=60) as response:
        data = json.loads(response.read().decode("utf-8"))

    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") == "output_text":
                return json.loads(content["text"])
    raise RuntimeError("OpenAI response did not contain output_text.")


def validate_brief(data: dict[str, str]) -> None:
    required = ["title", "one_line", "what_happened", "why_it_matters", "discussion_prompt"]
    for field in required:
        if not data.get(field):
            raise ValueError(f"Missing generated field: {field}")


def build_embed(brief: TrendBrief, track: str) -> discord.Embed:
    embed = discord.Embed(title=brief.title, description=brief.one_line, color=discord.Color.green())
    embed.add_field(name="무슨 내용인가", value=brief.what_happened, inline=False)
    embed.add_field(name="왜 중요한가", value=brief.why_it_matters, inline=False)
    embed.add_field(name="생각해볼 질문", value=brief.discussion_prompt, inline=False)
    embed.add_field(
        name="출처",
        value="\n".join(f"- {str(source['title'])}: {str(source['url'])}" for source in brief.sources),
        inline=False,
    )
    embed.add_field(name="주의", value=TREND_CAUTION_MESSAGE, inline=False)
    embed.set_footer(text=f"track={track} | mode=trend")
    return embed


def main() -> None:
    args = parse_args()
    history_path = Path(args.history_file)
    fetch_count = build_fetch_count(args.max_results)
    fetched_sources = fetch_trend_sources(track=args.track, max_results=fetch_count)
    history = load_history(history_path)
    try:
        sources = select_fresh_sources(
            track=args.track,
            fetched_sources=fetched_sources,
            history=history,
            max_results=args.max_results,
        )
    except NoFreshTrendSourcesError as exc:
        print(f"publish_status=skipped reason={exc}")
        return
    for source in sources:
        print(format_selection_log_line(args.track, source))
    bootstrap_pythonpath()
    from core.config import get_settings

    settings = get_settings()
    prompt = build_prompt(args.track, sources)
    if args.dry_run:
        print(f"dry_run track={args.track} source_count={len(sources)}")
        return
    api_key = getattr(settings, "openai_api_key", "") or __import__("os").getenv("OPENAI_API_KEY", "")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required.")
    if not settings.discord_webhook_url:
        raise RuntimeError("DISCORD_WEBHOOK_URL is required.")

    generated = generate_with_openai(prompt, api_key)
    validate_brief(generated)
    brief = TrendBrief(
        title=generated["title"],
        one_line=generated["one_line"],
        what_happened=generated["what_happened"],
        why_it_matters=generated["why_it_matters"],
        discussion_prompt=generated["discussion_prompt"],
        sources=sources,
    )
    embed = build_embed(brief, args.track)
    webhook = discord.SyncWebhook.from_url(settings.discord_webhook_url)
    message = webhook.send(content=f"오늘의 동향 브리핑 - {args.track}", embed=embed, wait=True)
    update_history(history_path, args.track, brief.title, sources)
    print(f"publish_status=success discord_message_id={message.id} track={args.track}")


if __name__ == "__main__":
    main()
