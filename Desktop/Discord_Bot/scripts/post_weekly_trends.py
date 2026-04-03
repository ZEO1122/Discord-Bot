from __future__ import annotations

# pyright: reportMissingImports=false

import argparse
from dataclasses import dataclass
import json
import os
from pathlib import Path
import sys

import discord
import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    from scripts.post_trend_brief import (
        TREND_CAUTION_MESSAGE,
        TrendBrief,
        build_fetch_count,
        build_prompt,
        format_selection_log_line,
        generate_with_openai,
        load_history,
        select_fresh_sources,
        update_history,
        validate_brief,
    )
    from scripts.fetch_trend_sources import fetch_trend_sources
except ImportError:
    from post_trend_brief import (
        TREND_CAUTION_MESSAGE,
        TrendBrief,
        build_fetch_count,
        build_prompt,
        format_selection_log_line,
        generate_with_openai,
        load_history,
        select_fresh_sources,
        update_history,
        validate_brief,
    )
    from fetch_trend_sources import fetch_trend_sources


@dataclass(slots=True)
class ChannelConfig:
    channel_key: str
    channel_id: str
    webhook_key: str
    enabled: bool
    interests: list[str]
    max_topics: int


@dataclass(slots=True)
class InterestSection:
    interest: str
    brief: TrendBrief


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Post weekly trend briefs to configured channels.")
    parser.add_argument("--channel-map-file", default="config/channel_interest_map.json")
    parser.add_argument("--history-file", default="content/trends/history/published_trends.json")
    parser.add_argument("--channel-key", default="")
    parser.add_argument("--max-results", type=int, default=3)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def load_channel_map(path: Path) -> list[ChannelConfig]:
    data = json.loads(path.read_text(encoding="utf-8"))
    raw_channels = data.get("channels", [])
    if not isinstance(raw_channels, list) or not raw_channels:
        raise RuntimeError("channel_interest_map.json must contain at least one channel.")
    channels: list[ChannelConfig] = []
    for item in raw_channels:
        channels.append(
            ChannelConfig(
                channel_key=str(item["channel_key"]),
                channel_id=str(item["channel_id"]),
                webhook_key=str(item["webhook_key"]),
                enabled=bool(item.get("enabled", True)),
                interests=[str(interest) for interest in item.get("interests", [])],
                max_topics=int(item.get("max_topics", 2)),
            )
        )
    return channels


def load_webhook_map() -> dict[str, str]:
    raw_map = os.getenv("DISCORD_WEBHOOK_MAP_JSON", "")
    if raw_map:
        try:
            parsed = json.loads(raw_map)
        except json.JSONDecodeError:
            parsed = yaml.safe_load(raw_map)
        if not isinstance(parsed, dict) or not parsed:
            raise RuntimeError("DISCORD_WEBHOOK_MAP_JSON must be a non-empty JSON object.")
        return {str(key): str(value) for key, value in parsed.items()}
    fallback_webhook = os.getenv("DISCORD_WEBHOOK_URL", "")
    if fallback_webhook:
        return {"default": fallback_webhook}
    raise RuntimeError("DISCORD_WEBHOOK_MAP_JSON or DISCORD_WEBHOOK_URL is required.")


def history_key(channel_id: str, interest: str) -> str:
    return f"{channel_id}:{interest}"


def build_channel_embed(channel: ChannelConfig, sections: list[InterestSection]) -> discord.Embed:
    embed = discord.Embed(
        title=f"이번 주 관심분야 브리핑 | {channel.channel_key}",
        description="채널 관심분야 기준으로 최신 동향을 묶어 전송합니다.",
        color=discord.Color.gold(),
    )
    for section in sections:
        source_lines = "\n".join(f"- {source['title']}: {source['url']}" for source in section.brief.sources[:2])
        embed.add_field(
            name=section.interest.upper(),
            value=(
                f"제목: {section.brief.title}\n"
                f"한 줄 요약: {section.brief.one_line}\n"
                f"왜 중요한가: {section.brief.why_it_matters}\n"
                f"출처:\n{source_lines}"
            ),
            inline=False,
        )
    embed.add_field(name="주의", value=TREND_CAUTION_MESSAGE, inline=False)
    return embed


def build_interest_brief(track: str, sources: list[dict[str, str]], api_key: str) -> TrendBrief:
    prompt = build_prompt(track, sources)
    generated = generate_with_openai(prompt, api_key)
    validate_brief(generated)
    return TrendBrief(
        title=generated["title"],
        one_line=generated["one_line"],
        what_happened=generated["what_happened"],
        why_it_matters=generated["why_it_matters"],
        discussion_prompt=generated["discussion_prompt"],
        sources=sources,
    )


def post_channel_embed(webhook_url: str, channel: ChannelConfig, embed: discord.Embed) -> str:
    webhook = discord.SyncWebhook.from_url(webhook_url)
    message = webhook.send(content=f"이번 주 관심분야 브리핑 - {channel.channel_key}", embed=embed, wait=True)
    return str(message.id)


def main() -> None:
    args = parse_args()
    channel_map = load_channel_map(Path(args.channel_map_file))
    webhook_map = load_webhook_map()
    history_path = Path(args.history_file)
    history = load_history(history_path)
    api_key = os.getenv("OPENAI_API_KEY", "")

    if not args.dry_run and not api_key:
        raise RuntimeError("OPENAI_API_KEY is required.")

    channels = [channel for channel in channel_map if channel.enabled]
    if args.channel_key:
        channels = [channel for channel in channels if channel.channel_key == args.channel_key]

    if not channels:
        if args.channel_key:
            raise RuntimeError(
                f"No enabled channel matched channel_key={args.channel_key}. "
                "Check config/channel_interest_map.json and enabled flags."
            )
        raise RuntimeError(
            "No enabled trend channels configured. "
            "Set enabled=true in config/channel_interest_map.json before running the workflow."
        )

    posted_channels = 0
    skipped_channels = 0
    for channel in channels:
        sections: list[InterestSection] = []
        for interest in channel.interests[: channel.max_topics]:
            fetched_sources = fetch_trend_sources(track=interest, max_results=build_fetch_count(args.max_results))
            scoped_history = {interest: history.get(history_key(channel.channel_id, interest), [])}
            try:
                fresh_sources = select_fresh_sources(
                    track=interest,
                    fetched_sources=fetched_sources,
                    history=scoped_history,
                    max_results=args.max_results,
                )
            except Exception:
                continue

            if args.dry_run:
                brief = TrendBrief(
                    title=f"{interest.upper()} 최신 동향",
                    one_line="dry-run 요약입니다.",
                    what_happened="최신 source를 수집해 브리핑 초안을 만들 수 있습니다.",
                    why_it_matters="운영 전 채널별 묶음 포맷을 검증하기 위함입니다.",
                    discussion_prompt="이 분야에서 이번 주 가장 주목할 점은 무엇일까?",
                    sources=fresh_sources,
                )
            else:
                brief = build_interest_brief(interest, fresh_sources, api_key)
            for source in fresh_sources:
                print(format_selection_log_line(interest, source))
            sections.append(InterestSection(interest=interest, brief=brief))

        if not sections:
            skipped_channels += 1
            print(f"channel_status=skipped channel_key={channel.channel_key} reason=no_fresh_sections")
            continue

        embed = build_channel_embed(channel, sections)
        if args.dry_run:
            print(f"channel_status=dry_run channel_key={channel.channel_key} section_count={len(sections)}")
            continue

        webhook_url = webhook_map.get(channel.webhook_key)
        if not webhook_url:
            raise RuntimeError(f"Missing webhook mapping for webhook_key={channel.webhook_key}")
        message_id = post_channel_embed(webhook_url, channel, embed)
        for section in sections:
            key = history_key(channel.channel_id, section.interest)
            existing = history.get(key, [])
            update_history(history_path, key, section.brief.title, section.brief.sources)
            history[key] = load_history(history_path).get(key, existing)
        posted_channels += 1
        print(f"channel_status=success channel_key={channel.channel_key} message_id={message_id} section_count={len(sections)}")

    if posted_channels == 0 and skipped_channels > 0:
        print("publish_status=skipped reason=no_channels_with_fresh_sections")
    else:
        print(f"publish_status=success posted_channels={posted_channels} skipped_channels={skipped_channels}")


if __name__ == "__main__":
    main()
