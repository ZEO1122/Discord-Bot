# Operations — GAS 운영 가이드

## 설정값

Apps Script `Script Properties` 필수값:
- `DISCORD_WEBHOOK_URL`
- `TREND_WEBHOOK_URL`
- `OPENAI_API_KEY`
- `OPENAI_MODEL`
- `GITHUB_RAW_BASE_URL`
- `CONCEPT_MANIFEST_PATH`
- `TREND_CONFIG_PATH`
- `TREND_HISTORY_SHEET_ID`
- `TREND_HISTORY_SHEET_NAME`

## 트리거

- concept: `runConceptDaily` / 평일 오전 9시 KST
- trend: `runTrendWeekly` / 월요일 오전 9시 KST

## 로그 확인

위치:
- Apps Script `Executions`
- 상세 `Logs`

### concept 로그
- `runConceptDaily:start`
- `runConceptDaily:success`

### trend 로그
- `runTrendWeekly:start`
- `TrendService:recent_papers count=...`
- `TrendService:top_papers count=...`
- `OpenAIService:classify request ...`
- `OpenAIService:request model=...`
- `TrendService:posted sections=...`

## 재시도 정책

- concept 실패: `runConceptDaily()` 재실행
- trend 실패: OpenAlex fetch / OpenAI / trend webhook / Sheets 확인 후 재실행
- fresh paper 없음: 정상 skip 가능

## 유지보수 포인트

### concept
- `content/concepts/**/*.md`
- `content/concepts/manifest.json`

### trend
- `config/trend_brief_config.json`
- Google Sheets `trend_history`

## 운영 체크리스트

- [ ] `runConceptDaily()` 수동 실행 성공
- [ ] `runTrendWeekly()` 수동 실행 성공
- [ ] Script Properties 설정 완료
- [ ] `trend_brief_config.json` 실제 값 반영 완료
- [ ] `trend_history` 시트 연결 완료
