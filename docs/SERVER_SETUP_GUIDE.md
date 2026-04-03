# Server Setup Guide

## 목표
- concept 브리핑은 평일 오전 9시 KST에 자동 게시
- trend 브리핑은 월요일 오전 9시 KST에 최근 7일 고인용 논문 상위 3편을 자동 게시
- 자동화는 Google Apps Script + Discord Webhook으로 운영

## 준비물
- GitHub public 저장소 접근 권한
- Google Apps Script 프로젝트 접근 권한
- Discord concept 채널 1개
- Discord 공용 trend 채널 1개
- OpenAI API key
- Google Sheets 1개

## Script Properties
- `DISCORD_WEBHOOK_URL`
- `TREND_WEBHOOK_URL`
- `OPENAI_API_KEY`
- `OPENAI_MODEL`
- `GITHUB_RAW_BASE_URL`
- `CONCEPT_MANIFEST_PATH`
- `TREND_CONFIG_PATH`
- `TREND_HISTORY_SHEET_ID`
- `TREND_HISTORY_SHEET_NAME`

## trend 설정 파일
- `config/trend_brief_config.json`

예시:

```json
{
  "version": 1,
  "timezone": "Asia/Seoul",
  "lookback_days": 7,
  "top_papers": 3,
  "source_provider": "openalex",
  "search_query": "artificial intelligence machine learning deep learning",
  "taxonomy": ["llm", "detection-segmentation", "vision-language", "other"]
}
```

## 수동 검증
- `runConceptDaily()`
- `runTrendWeekly()`

## 자동 스케줄
- concept: 평일 오전 9시 KST
- trend: 월요일 오전 9시 KST
