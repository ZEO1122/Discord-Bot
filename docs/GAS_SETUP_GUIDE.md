# GAS Setup Guide

## 준비물
- Google 계정
- GitHub public 저장소
- Discord webhook 2개
  - concept 채널
  - 공용 trend 채널
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

예시:

```text
OPENAI_MODEL=gpt-5.1
GITHUB_RAW_BASE_URL=https://raw.githubusercontent.com/<OWNER>/<REPO>/main
CONCEPT_MANIFEST_PATH=content/concepts/manifest.json
TREND_CONFIG_PATH=config/trend_brief_config.json
TREND_HISTORY_SHEET_NAME=trend_history
```

## Google Sheets 준비

탭 이름:
- `trend_history`

헤더:

```text
paper_id | title | canonical_url | published_at | citation_count | topic_tag | posted_at | brief_title
```

## GitHub raw에서 읽는 파일
- `content/concepts/manifest.json`
- `content/concepts/**/*.md`
- `config/trend_brief_config.json`

## 수동 실행
- `runConceptDaily()`
- `runTrendWeekly()`

## 트리거
- concept: 평일 오전 9시 KST
- trend: 월요일 오전 9시 KST
