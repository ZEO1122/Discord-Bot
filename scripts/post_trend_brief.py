from __future__ import annotations

# pyright: reportMissingImports=false

import argparse
from dataclasses import dataclass
from datetime import UTC, datetime
import json
from pathlib import Path
import sys
from urllib import request

import discord

try:
    from scripts.fetch_trend_sources import fetch_trend_sources
except ImportError:
    from fetch_trend_sources import fetch_trend_sources


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
    sources: list[dict[str, str]]


def normalize_source_url(url: str) -> str:
    normalized = url.strip()
    if "arxiv.org/abs/" in normalized:
        prefix, arxiv_id = normalized.split("/abs/", 1)
        arxiv_id = arxiv_id.split("?", 1)[0]
        if "v" in arxiv_id and arxiv_id.rsplit("v", 1)[-1].isdigit():
            arxiv_id = arxiv_id.rsplit("v", 1)[0]
        return f"{prefix}/abs/{arxiv_id}"
    return normalized


def load_history(history_path: Path) -> dict[str, list[dict[str, str]]]:
    if not history_path.exists():
        return {}
    return json.loads(history_path.read_text(encoding="utf-8"))


def select_fresh_sources(
    track: str,
    fetched_sources: list[dict[str, str]],
    history: dict[str, list[dict[str, str]]],
    max_results: int,
) -> list[dict[str, str]]:
    seen_urls = {normalize_source_url(item["url"]) for item in history.get(track, [])}
    fresh_sources = [source for source in fetched_sources if normalize_source_url(source["url"]) not in seen_urls]
    if not fresh_sources:
        raise RuntimeError(f"No fresh trend sources available for track={track}")
    return fresh_sources[:max_results]


def update_history(
    history_path: Path,
    track: str,
    generated_title: str,
    selected_sources: list[dict[str, str]],
) -> None:
    history = load_history(history_path)
    track_history = history.get(track, [])
    posted_at = datetime.now(UTC).isoformat()
    for source in selected_sources:
        track_history.append(
            {
                "title": generated_title,
                "source_title": source["title"],
                "url": normalize_source_url(source["url"]),
                "published_at": source.get("published_at", ""),
                "posted_at": posted_at,
            }
        )
    history[track] = track_history[-50:]
    history_path.parent.mkdir(parents=True, exist_ok=True)
    history_path.write_text(json.dumps(history, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_prompt(track: str, sources: list[dict[str, str]]) -> str:
    source_lines = "\n".join(f"- {item['title']} | {item['url']} | {item.get('published_at', '')}" for item in sources)
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
    payload = {
        "model": "gpt-4.1-mini",
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
        value="\n".join(f"- {source['title']}: {source['url']}" for source in brief.sources),
        inline=False,
    )
    embed.set_footer(text=f"track={track} | mode=trend")
    return embed


def main() -> None:
    args = parse_args()
    history_path = Path(args.history_file)
    fetch_count = min(max(args.max_results + 3, args.max_results), 10)
    fetched_sources = fetch_trend_sources(track=args.track, max_results=fetch_count)
    history = load_history(history_path)
    sources = select_fresh_sources(
        track=args.track,
        fetched_sources=fetched_sources,
        history=history,
        max_results=args.max_results,
    )
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
