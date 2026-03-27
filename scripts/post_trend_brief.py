from __future__ import annotations

# pyright: reportMissingImports=false

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
import sys
from urllib import request

import discord

from fetch_trend_sources import fetch_trend_sources


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate and post a trend brief to Discord.")
    parser.add_argument("--track", required=True)
    parser.add_argument("--max-results", type=int, default=5)
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
    sources = fetch_trend_sources(track=args.track, max_results=args.max_results)
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
    print(f"publish_status=success discord_message_id={message.id} track={args.track}")


if __name__ == "__main__":
    main()
