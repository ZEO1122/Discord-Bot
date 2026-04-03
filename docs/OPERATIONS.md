# Operations — GAS 운영 가이드

## 1. 운영 기본값

- concept: `runConceptDaily` / 평일 오전 9시 KST
- trend: `runTrendWeekly` / 월요일 오전 9시 KST
- 실행 방식: Google Apps Script + Discord Webhook

## 2. 필수 운영 자산

### concept
- `content/concepts/**/*.md`
- `content/concepts/manifest.json`

### trend
- `config/trend_brief_config.json`
- Google Sheets `trend_history`

### Script Properties
- `DISCORD_WEBHOOK_URL`
- `TREND_WEBHOOK_URL`
- `OPENAI_API_KEY`
- `OPENAI_MODEL`
- `GITHUB_RAW_BASE_URL`
- `CONCEPT_MANIFEST_PATH`
- `TREND_CONFIG_PATH`
- `TREND_HISTORY_SHEET_ID`
- `TREND_HISTORY_SHEET_NAME`

## 3. 로그 확인

위치:

- Apps Script `Executions`
- 상세 `Logs`

중요 로그:

### concept
- `runConceptDaily:start`
- `runConceptDaily:success`

### trend
- `runTrendWeekly:start`
- `TrendService:recent_papers count=...`
- `TrendService:top_papers count=...`
- `OpenAIService:classify request ...`
- `OpenAIService:request model=...`
- `TrendService:posted sections=...`

## 4. 재시도 정책

- concept 실패: `runConceptDaily()` 재실행
- trend 실패: OpenAlex fetch, OpenAI, webhook, Sheets 확인 후 `runTrendWeekly()` 재실행
- fresh paper 없음: 정상 skip 가능

## 5. 유지보수 루틴

### concept 추가/수정
1. `.md` 작성 또는 수정
2. `manifest.json` 순서 반영
3. `clasp push`
4. `runConceptDaily()` 수동 검증

### trend 설정 수정
1. `config/trend_brief_config.json` 수정
2. 필요한 값 점검
   - `lookback_days`
   - `top_papers`
   - `candidate_pool_size`
   - `search_query`
   - `taxonomy`
3. `clasp push`
4. `runTrendWeekly()` 수동 검증

trend 선정은 아래 기준으로 점검한다.

- 후보가 반드시 지난 7일 논문으로만 잡히는지
- 같은 기간 안에서 citation_count가 높은 논문이 상위에 오는지
- history 기준 중복 제거가 동작하는지

## 6. 운영 서버 전환 체크리스트

운영 서버 또는 새 Discord 서버로 옮길 때는 아래만 교체하면 된다.

1. Script Properties 값을 운영 기준으로 교체
2. `trend_brief_config.json`을 운영 기준으로 수정
3. concept progress reset 여부 결정
4. trend history 시트 정리 여부 결정
5. `runConceptDaily()` 수동 실행
6. `runTrendWeekly()` 수동 실행
7. 결과 확인 후 time trigger 운영 시작

## 7. 운영 체크리스트

- [ ] `runConceptDaily()` 수동 실행 성공
- [ ] `runTrendWeekly()` 수동 실행 성공
- [ ] Script Properties 설정 완료
- [ ] `trend_brief_config.json` 실제 값 반영 완료
- [ ] `trend_history` 시트 연결 완료
- [ ] Apps Script 로그에서 실패 지점 확인 가능
