# GAS Import Checklist

## Apps Script에 넣을 파일 순서
1. `appsscript.json`
2. `ConfigService.gs`
3. `GitHubService.gs`
4. `Utils.gs`
5. `DiscordService.gs`
6. `HistoryService.gs`
7. `OpenAIService.gs`
8. `ConceptService.gs`
9. `TrendService.gs`
10. `Code.gs`

## Script Properties 입력
- `DISCORD_WEBHOOK_URL`
- `TREND_WEBHOOK_URL`
- `OPENAI_API_KEY`
- `OPENAI_MODEL`
- `GITHUB_RAW_BASE_URL`
- `CONCEPT_MANIFEST_PATH`
- `TREND_CONFIG_PATH`
- `TREND_HISTORY_SHEET_ID`
- `TREND_HISTORY_SHEET_NAME`

## 수동 검증 순서
1. `runConceptDaily()`
2. concept 채널 확인
3. Script Properties progress 확인
4. `runTrendWeekly()`
5. 공용 trend 채널 확인
6. Google Sheets `trend_history` 확인
