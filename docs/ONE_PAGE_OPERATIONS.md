# One-Page Operations

## 이 프로젝트가 하는 일
- 평일 오전 9시 KST: concept 브리핑 1개 자동 게시
- 월요일 오전 9시 KST: 최근 7일 고인용 논문 상위 3편 자동 게시
- 실행 방식: Google Apps Script + Discord Webhook

## 먼저 볼 파일
- `content/concepts/manifest.json`
- `config/trend_brief_config.json`
- `docs/SERVER_SETUP_GUIDE.md`
- `docs/OPERATIONS.md`

## 필수 Script Properties
- `DISCORD_WEBHOOK_URL`
- `TREND_WEBHOOK_URL`
- `OPENAI_API_KEY`
- `OPENAI_MODEL`
- `GITHUB_RAW_BASE_URL`
- `CONCEPT_MANIFEST_PATH`
- `TREND_CONFIG_PATH`
- `TREND_HISTORY_SHEET_ID`
- `TREND_HISTORY_SHEET_NAME`

## 수동 테스트
- `runConceptDaily()`
- `runTrendWeekly()`

## 운영자용 한 줄 요약
- concept는 `manifest.json`만 보면 된다
- trend는 `trend_brief_config.json`만 보면 된다
- 문제 생기면 Apps Script `Executions` 로그부터 본다
