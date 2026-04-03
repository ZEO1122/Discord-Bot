# Club Server Transition Checklist

## 전환 원칙
- 코드와 GAS 구조는 그대로 유지한다.
- Discord webhook, 운영 설정, history 저장소는 운영 서버 기준으로 교체하거나 초기화한다.

## 그대로 유지해도 되는 것
- `apps-script/*.gs`
- `content/concepts/**/*.md`
- `content/concepts/manifest.json`
- 운영 문서 전반

## 운영 서버 기준으로 교체해야 하는 것

### Apps Script Script Properties
- `DISCORD_WEBHOOK_URL`
- `TREND_WEBHOOK_URL`
- `OPENAI_API_KEY`
- `TREND_HISTORY_SHEET_ID`
- `TREND_HISTORY_SHEET_NAME`

### trend 설정 파일
- `config/trend_brief_config.json`
- 확인할 값:
  - `lookback_days`
  - `top_papers`
  - `source_provider`
  - `search_query`
  - `taxonomy`

## reset 권장 항목

### concept 진행 상태
- 저장 위치: Script Properties
- 처음부터 다시 보내고 싶으면 reset

### trend history
- 저장 위치: Google Sheets
- 테스트 흔적을 없애고 싶으면 시트 row 정리

## 전환 절차
1. Apps Script `Script Properties`를 운영 서버 기준으로 교체
2. `trend_brief_config.json`을 운영 기준으로 수정
3. taxonomy를 아래 4개로 맞춘다.
   - `llm`
   - `detection-segmentation`
   - `vision-language`
   - `other`
4. concept progress reset 여부 결정
5. trend history Sheet 정리 여부 결정
6. `runConceptDaily()` 수동 실행
7. `runTrendWeekly()` 수동 실행
8. 결과가 맞으면 time trigger 운영 시작
