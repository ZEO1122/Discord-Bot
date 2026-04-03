# Maintenance Guide

## concept 유지보수
- `content/concepts/**/*.md`
- `content/concepts/manifest.json`

새 concept 추가:
1. `.md` 작성
2. `manifest.json` 마지막에 경로 추가
3. `clasp push`
4. `runConceptDaily()` 수동 검증

## trend 유지보수
- `config/trend_brief_config.json`

바꿀 수 있는 값:
- `lookback_days`
- `top_papers`
- `search_query`
- `taxonomy`

수정 후:
1. `clasp push`
2. `runTrendWeekly()` 수동 검증

## Script Properties 유지보수
- `DISCORD_WEBHOOK_URL`
- `TREND_WEBHOOK_URL`
- `OPENAI_API_KEY`
- `OPENAI_MODEL`
- `GITHUB_RAW_BASE_URL`
- `CONCEPT_MANIFEST_PATH`
- `TREND_CONFIG_PATH`
- `TREND_HISTORY_SHEET_ID`
- `TREND_HISTORY_SHEET_NAME`

## 운영 중 확인할 것
- Apps Script `Executions`
- Google Sheets `trend_history`
- Discord concept/trend 채널
