from __future__ import annotations

import json
from pathlib import Path
from typing import cast

from scripts.post_weekly_trends import (
    DISCORD_EMBED_FIELD_VALUE_LIMIT,
    InterestSection,
    build_channel_embed,
    format_section_value,
    history_key,
    load_channel_map,
    load_webhook_map,
)
from scripts.post_trend_brief import TrendBrief


def test_history_key_uses_channel_and_interest() -> None:
    assert history_key("123", "nlp") == "123:nlp"


def test_load_channel_map_parses_channels(tmp_path: Path) -> None:
    config_path = tmp_path / "channel_interest_map.json"
    config_path.write_text(
        json.dumps(
            {
                "channels": [
                    {
                        "channel_key": "default-channel",
                        "channel_id": "123",
                        "webhook_key": "default",
                        "enabled": True,
                        "interests": ["nlp", "llm"],
                        "max_topics": 2,
                    }
                ]
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    channels = load_channel_map(config_path)
    assert len(channels) == 1
    assert channels[0].channel_key == "default-channel"
    assert channels[0].interests == ["nlp", "llm"]


def test_build_channel_embed_bundles_interest_sections() -> None:
    config_path = Path("/tmp/channel_interest_map_test.json")
    config_path.write_text(
        json.dumps(
            {
                "channels": [
                    {
                        "channel_key": "default-channel",
                        "channel_id": "123",
                        "webhook_key": "default",
                        "enabled": True,
                        "interests": ["nlp"],
                        "max_topics": 1,
                    }
                ]
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    channel = load_channel_map(config_path)[0]
    sections = [
        InterestSection(
            interest="nlp",
            brief=TrendBrief(
                title="NLP 동향",
                one_line="LLM 추론 논문이 증가하고 있다.",
                what_happened="최근 논문이 증가했다.",
                why_it_matters="응용이 늘어난다.",
                discussion_prompt="이번 주 핵심은?",
                sources=[{"title": "Paper", "url": "https://arxiv.org/abs/1234.5678"}],
            ),
        )
    ]
    embed = build_channel_embed(channel, sections)
    assert "이번 주 관심분야 브리핑" in (embed.title or "")
    assert embed.fields[-1].name == "주의"


def test_load_webhook_map_uses_fallback(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.delenv("DISCORD_WEBHOOK_MAP_JSON", raising=False)
    monkeypatch.setenv("DISCORD_WEBHOOK_URL", "https://discord.com/api/webhooks/test")
    assert load_webhook_map() == {"default": "https://discord.com/api/webhooks/test"}


def test_load_webhook_map_accepts_yaml_style_secret(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.setenv(
        "DISCORD_WEBHOOK_MAP_JSON",
        "default: https://discord.com/api/webhooks/test\nnlp-study: https://discord.com/api/webhooks/test2\n",
    )
    assert load_webhook_map() == {
        "default": "https://discord.com/api/webhooks/test",
        "nlp-study": "https://discord.com/api/webhooks/test2",
    }


def test_load_channel_map_preserves_disabled_channels(tmp_path: Path) -> None:
    config_path = tmp_path / "channel_interest_map.json"
    config_path.write_text(
        json.dumps(
            {
                "channels": [
                    {
                        "channel_key": "llm-brief",
                        "channel_id": "123",
                        "webhook_key": "llm-brief",
                        "enabled": False,
                        "interests": ["llm"],
                        "max_topics": 1,
                    }
                ]
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    channels = load_channel_map(config_path)
    assert len(channels) == 1
    assert channels[0].enabled is False


def test_format_section_value_truncates_long_content_to_embed_limit() -> None:
    value = format_section_value(
        title="긴 제목 " * 30,
        one_line="긴 요약 " * 80,
        why_it_matters="긴 중요성 설명 " * 120,
        source_lines=["- Source A: https://example.com/very/long/url" * 5],
    )
    assert len(value) <= DISCORD_EMBED_FIELD_VALUE_LIMIT
    assert "제목:" in value
    assert "한 줄 요약:" in value


def test_build_channel_embed_keeps_field_values_within_limit() -> None:
    config_path = Path("/tmp/channel_interest_map_long_test.json")
    config_path.write_text(
        json.dumps(
            {
                "channels": [
                    {
                        "channel_key": "llm-brief",
                        "channel_id": "123",
                        "webhook_key": "llm-brief",
                        "enabled": True,
                        "interests": ["llm"],
                        "max_topics": 1,
                    }
                ]
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    channel = load_channel_map(config_path)[0]
    sections = [
        InterestSection(
            interest="llm",
            brief=TrendBrief(
                title="긴 제목 " * 30,
                one_line="긴 요약 " * 80,
                what_happened="최근 연구가 증가했다.",
                why_it_matters="긴 중요성 설명 " * 120,
                discussion_prompt="토론 질문",
                sources=[
                    {"title": "Very Long Paper Title " * 10, "url": "https://example.com/very/long/url" * 3},
                    {"title": "Another Long Paper Title " * 10, "url": "https://example.com/another/long/url" * 3},
                ],
            ),
        )
    ]
    embed = build_channel_embed(channel, sections)
    assert len(cast(str, embed.fields[0].value)) <= DISCORD_EMBED_FIELD_VALUE_LIMIT
