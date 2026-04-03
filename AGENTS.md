# AGENTS.md

## Purpose
This repo is a Discord briefing automation repository for an AI study club.
It uses Google Apps Script for scheduling and Discord Webhook for delivery.

## Current State
- Main contents are `README.md`, `FILE_TREE.md`, `docs/*.md`, `apps-script/`, `content/`, and `config/`.
- The checked-in runtime implementation lives in `apps-script/`.
- `FILE_TREE.md` should be kept in sync with the implemented structure.
- Ignore `.DS_Store` and `._*` files.

## Product Priorities
Optimize in this order: accuracy, traceability, operational simplicity.

## Read Before Larger Changes
Read the relevant docs before implementing:
- `README.md`
- `docs/ARCHITECTURE.md`
- `docs/CONTENT_PIPELINE.md`
- `docs/DATABASE_SCHEMA.md`
- `docs/OPERATIONS.md`
- `docs/ROADMAP.md`
- `docs/GAS_SETUP_GUIDE.md`
- `docs/GAS_IMPORT_CHECKLIST.md`
- `docs/GAS_FINAL_CHECKLIST.md`
- `docs/MAINTENANCE_GUIDE.md`

For publishing, content pipeline, or operations changes, read the matching doc first.

## Non-Negotiable Domain Rules
- Store source metadata structurally, not as one display string.
- Keep concept progress and trend history traceable.
- Do not log webhook URLs, API keys, or other secrets.
- Do not auto-publish a trend briefing that has no sources.

## Preferred Stack
Use Google Apps Script for scheduled execution, Discord Webhook for delivery, GitHub public repo for content/config source, and Google Sheets/Script Properties for lightweight state.

## Target Layout
Follow the implemented `apps-script`, `content`, `config`, and `docs` layout from `README.md`.
Keep GAS entrypoints, external fetches, payload construction, and history storage logically separate.

## Commands

### Apps Script
```bash
npm install
npx clasp login
npx clasp status
npx clasp push
npx clasp pull
npx clasp open
```

## Workflow
- Plan first for content pipeline, configuration, or operations changes.
- Update the relevant docs whenever behavior, architecture, or operations change.

## Code Style Guidelines

### Naming
- Use English for code identifiers, module names, and filenames.
- Use Korean for most user-facing strings.
- Use descriptive service names such as `ConceptService`, `TrendService`, and `HistoryService`.

### Design
- Keep GAS entrypoints thin.
- Separate GitHub raw fetch, OpenAI calls, Discord posting, and history storage concerns.
- Make duplicate-post policy explicit.

### Error Handling And Security
- Fail loudly for invariant violations.
- Never swallow exceptions silently.
- Log enough context to debug publish failures without logging secrets.
- Never hardcode webhook URLs or API keys.

## Testing Expectations
- Prefer deterministic helpers and narrow service-level checks when editing Apps Script logic.
- Keep operational behavior easy to validate through manual GAS runs and logs.

## Documentation Sync Rules
Update the matching docs when these areas change:
- Concept/trend pipeline rules -> `docs/CONTENT_PIPELINE.md`
- State storage or history columns -> `docs/DATABASE_SCHEMA.md`
- Architecture or service boundaries -> `docs/ARCHITECTURE.md`
- Deployment or runtime operations -> `docs/OPERATIONS.md`
- Scope or MVP definition -> `docs/PRD.md` or `docs/ROADMAP.md`

## Practical Reminders
- Start from the docs and be explicit about ops impact.
- Prefer incremental, traceable changes over speculative scaffolding.
