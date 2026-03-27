from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import sys
from typing import Any

import discord
import yaml


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Post a concept markdown brief to Discord.")
    parser.add_argument("--brief-path", required=True)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def bootstrap_pythonpath() -> None:
    root = Path(__file__).resolve().parents[1]
    src = root / "src"
    if str(src) not in sys.path:
        sys.path.insert(0, str(src))


@dataclass(slots=True)
class ParsedBrief:
    briefing_key: str
    track: str
    title: str
    one_line: str
    discussion_prompt: str | None
    what_happened: str
    why_it_matters: str
    easy_terms: list[str]
    sources: list[dict[str, str]]


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("Markdown must start with YAML frontmatter.")
    _, rest = text.split("---\n", 1)
    frontmatter, body = rest.split("\n---\n", 1)
    return frontmatter, body.strip()


def extract_section(body: str, heading: str) -> str:
    marker = f"## {heading}\n"
    if marker not in body:
        raise ValueError(f"Missing section: {heading}")
    after = body.split(marker, 1)[1]
    next_index = after.find("\n## ")
    content = after if next_index == -1 else after[:next_index]
    return content.strip()


def extract_section_any(body: str, headings: list[str], *, required: bool = True) -> str:
    for heading in headings:
        marker = f"## {heading}\n"
        if marker in body:
            return extract_section(body, heading)
    if required:
        raise ValueError(f"Missing section: {' or '.join(headings)}")
    return ""


def parse_sources(meta: dict[str, Any], body: str) -> list[dict[str, str]]:
    raw_sources = meta.get("sources")
    if isinstance(raw_sources, list) and raw_sources:
        parsed_sources: list[dict[str, str]] = []
        for item in raw_sources:
            if isinstance(item, dict):
                parsed_sources.append(
                    {
                        "title": str(item.get("title", "")).strip(),
                        "url": str(item.get("url", "")).strip(),
                    }
                )
            else:
                parsed_sources.append({"title": str(item).strip(), "url": ""})
        return [source for source in parsed_sources if source["title"]]

    source_block = extract_section_any(body, ["출처", "source", "sources"], required=False)
    if not source_block:
        raise ValueError("Missing frontmatter field: sources")

    sources: list[dict[str, str]] = []
    for line in source_block.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        cleaned = stripped[1:].strip() if stripped.startswith("-") else stripped
        sources.append({"title": cleaned, "url": ""})
    if not sources:
        raise ValueError("Missing frontmatter field: sources")
    return sources


def parse_brief(path: Path) -> ParsedBrief:
    frontmatter_text, body = split_frontmatter(path.read_text(encoding="utf-8"))
    meta = yaml.safe_load(frontmatter_text)
    if not isinstance(meta, dict):
        raise ValueError("Frontmatter must be a mapping.")

    what_happened = extract_section_any(body, ["무슨 내용인가", "핵심 설명"])
    why_it_matters = extract_section_any(body, ["왜 중요한가", "직관", "헷갈리기 쉬운 점"])
    easy_terms_block = extract_section_any(body, ["쉬운 용어"], required=False)
    easy_terms = [line.strip("- ").strip() for line in easy_terms_block.splitlines() if line.strip()]
    sources = parse_sources(meta, body)

    required = ["briefing_key", "track", "title", "one_line"]
    for field in required:
        if not meta.get(field):
            raise ValueError(f"Missing frontmatter field: {field}")

    return ParsedBrief(
        briefing_key=str(meta["briefing_key"]),
        track=str(meta["track"]),
        title=str(meta["title"]),
        one_line=str(meta["one_line"]),
        discussion_prompt=meta.get("discussion_prompt"),
        what_happened=what_happened,
        why_it_matters=why_it_matters,
        easy_terms=easy_terms,
        sources=sources,
    )


def build_embed(brief: ParsedBrief) -> discord.Embed:
    embed = discord.Embed(title=brief.title, description=brief.one_line, color=discord.Color.blue())
    embed.add_field(name="무슨 내용인가", value=brief.what_happened, inline=False)
    embed.add_field(name="왜 중요한가", value=brief.why_it_matters, inline=False)
    if brief.easy_terms:
        embed.add_field(name="쉬운 용어", value="\n".join(f"- {item}" for item in brief.easy_terms), inline=False)
    embed.add_field(name="생각해볼 질문", value=brief.discussion_prompt or "아직 준비되지 않았습니다.", inline=False)
    embed.add_field(
        name="출처",
        value="\n".join(
            f"- {source['title']}: {source['url']}" if source.get("url") else f"- {source['title']}"
            for source in brief.sources
        ),
        inline=False,
    )
    return embed


def main() -> None:
    args = parse_args()
    brief = parse_brief(Path(args.brief_path))
    embed = build_embed(brief)
    if args.dry_run:
        print(f"dry_run briefing_key={brief.briefing_key} title={brief.title}")
        return

    bootstrap_pythonpath()
    from core.config import get_settings

    settings = get_settings()
    if not settings.discord_webhook_url:
        raise RuntimeError("DISCORD_WEBHOOK_URL is required.")
    webhook = discord.SyncWebhook.from_url(settings.discord_webhook_url)
    message = webhook.send(content=f"오늘의 브리핑 - {brief.track}", embed=embed, wait=True)
    print(f"publish_status=success discord_message_id={message.id} briefing_key={brief.briefing_key}")


if __name__ == "__main__":
    main()
