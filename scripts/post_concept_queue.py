from __future__ import annotations

# pyright: reportMissingImports=false

import argparse
from datetime import UTC, datetime
import json
from pathlib import Path

import discord

from scripts.post_concept_brief import ParsedBrief, build_embed, parse_brief


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Post the next concept brief from the manifest queue.")
    parser.add_argument("--manifest-file", default="content/concepts/manifest.json")
    parser.add_argument("--progress-file", default="content/concepts/history/concept_progress.json")
    parser.add_argument("--brief-path", default="")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def load_json(path: Path, default: dict[str, object]) -> dict[str, object]:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def load_manifest(path: Path) -> dict[str, object]:
    data = load_json(path, default={"order": []})
    order = data.get("order", [])
    if not isinstance(order, list) or not order:
        raise RuntimeError("Concept manifest must contain a non-empty 'order' list.")
    return data


def load_progress(path: Path) -> dict[str, object]:
    return load_json(
        path,
        default={
            "version": 1,
            "last_index": -1,
            "last_path": None,
            "last_briefing_key": None,
            "last_posted_at": None,
        },
    )


def select_next_brief_path(manifest: dict[str, object], progress: dict[str, object]) -> tuple[int, str] | None:
    order = manifest["order"]
    assert isinstance(order, list)
    last_index = int(progress.get("last_index", -1))
    next_index = last_index + 1
    if next_index >= len(order):
        return None
    next_path = order[next_index]
    if not isinstance(next_path, str):
        raise RuntimeError("Manifest order entries must be strings.")
    return next_index, next_path


def update_progress(progress_path: Path, index: int, path: str, brief: ParsedBrief) -> None:
    data = {
        "version": 1,
        "last_index": index,
        "last_path": path,
        "last_briefing_key": brief.briefing_key,
        "last_posted_at": datetime.now(UTC).isoformat(),
    }
    progress_path.parent.mkdir(parents=True, exist_ok=True)
    progress_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def post_embed(webhook_url: str, brief: ParsedBrief, embed: discord.Embed) -> str:
    webhook = discord.SyncWebhook.from_url(webhook_url)
    message = webhook.send(content=f"오늘의 브리핑 - {brief.track}", embed=embed, wait=True)
    return str(message.id)


def main() -> None:
    args = parse_args()
    from core.config import get_settings

    settings = get_settings()
    manifest_path = Path(args.manifest_file)
    progress_path = Path(args.progress_file)

    selected_index: int | None = None
    selected_path: str
    if args.brief_path:
        selected_path = args.brief_path
    else:
        manifest = load_manifest(manifest_path)
        progress = load_progress(progress_path)
        selection = select_next_brief_path(manifest, progress)
        if selection is None:
            print("publish_status=skipped reason=no_remaining_concepts")
            return
        selected_index, selected_path = selection

    brief = parse_brief(Path(selected_path))
    embed = build_embed(brief)
    if args.dry_run:
        print(f"publish_status=dry_run briefing_key={brief.briefing_key} path={selected_path}")
        return

    if not settings.discord_webhook_url:
        raise RuntimeError("DISCORD_WEBHOOK_URL is required.")

    message_id = post_embed(settings.discord_webhook_url, brief, embed)
    if selected_index is not None:
        update_progress(progress_path, selected_index, selected_path, brief)
    print(f"publish_status=success discord_message_id={message_id} briefing_key={brief.briefing_key}")


if __name__ == "__main__":
    main()
