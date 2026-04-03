# GAS Setup Guide

## 1. 준비물

- Google 계정
- GitHub public 저장소
- Discord webhook 2개
  - concept 채널
  - 공용 trend 채널
- OpenAI API key
- Google Sheets 1개

## 2. Apps Script에 넣을 파일 순서

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

## 3. Script Properties

필수 키:

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

## 4. Google Sheets 준비

탭 이름:

- `trend_history`

헤더:

```text
paper_id | title | canonical_url | published_at | citation_count | topic_tag | posted_at | brief_title
```

## 5. GitHub raw에서 읽는 파일

- `content/concepts/manifest.json`
- `content/concepts/**/*.md`
- `config/trend_brief_config.json`

## 6. trend 세부분야 의미

- `foundation-models`: Foundation Models(파운데이션 모델)
- `vision-perception`: Vision Perception(비전 인지)
- `multimodal-agents`: Multimodal Agents(멀티모달 에이전트)
- `speech-audio`: Speech and Audio(음성·오디오)
- `retrieval-search`: Retrieval and Search(검색·리트리벌)
- `robotics-embodied`: Robotics and Embodied AI(로보틱스·체화 AI)
- `generation-creative`: Generation and Creative(생성·크리에이티브)
- `data-training`: Data and Training(데이터·학습)
- `systems-efficiency`: Systems Efficiency(시스템 효율화)
- `other`: Other(기타)

## 7. 수동 검증 순서

1. `runConceptDaily()`
2. concept 채널 확인
3. Script Properties progress 확인
4. `runTrendWeekly()`
5. 공용 trend 채널 확인
6. Google Sheets `trend_history` 확인

## 8. 최종 체크리스트

- [ ] `DISCORD_WEBHOOK_URL` 입력 완료
- [ ] `TREND_WEBHOOK_URL` 입력 완료
- [ ] `OPENAI_API_KEY` 입력 완료
- [ ] `OPENAI_MODEL` 확인
- [ ] `GITHUB_RAW_BASE_URL` 입력 완료
- [ ] `CONCEPT_MANIFEST_PATH` 확인
- [ ] `TREND_CONFIG_PATH` 확인
- [ ] `TREND_HISTORY_SHEET_ID` 입력 완료
- [ ] `TREND_HISTORY_SHEET_NAME=trend_history` 확인
- [ ] concept 채널 webhook 확인
- [ ] 공용 trend 채널 webhook 확인
- [ ] `trend_brief_config.json` 값 확인

## 9. 트리거

- concept: 평일 오전 9시 KST
- trend: 월요일 오전 9시 KST
