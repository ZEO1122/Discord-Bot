# Database Schema — GAS 상태 저장 구조

## 1. 문서 목적

이 문서는 현재 GAS 기반 운영에서 사용하는 상태 저장 구조를 정리한다.

현재 레포는 로컬 DB를 사용하지 않고, Script Properties와 Google Sheets를 운영 상태 저장소로 사용한다.

## 2. 저장 원칙

- concept 진행 상태는 Script Properties에 저장한다.
- trend 게시 이력은 Google Sheets에 저장한다.
- content 원본과 설정 원본은 GitHub 저장소에 둔다.
- Discord 메시지 추적에 필요한 최소 정보만 저장한다.

## 3. 저장 위치

### 3.1 GitHub 저장소
- `content/concepts/**/*.md`
- `content/concepts/manifest.json`
- `config/trend_brief_config.json`

### 3.2 Script Properties
- concept 진행 상태
- webhook 및 API 설정
- GitHub raw 경로 설정

### 3.3 Google Sheets
- trend 게시 history

## 4. Script Properties

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

concept 진행 상태 예시:

```json
{
  "lastIndex": 12,
  "lastPath": "content/concepts/dl-basics/dl-concept-013-learning-rate.md",
  "lastBriefingKey": "dl-concept-013-learning-rate",
  "lastPostedAt": "2026-04-03T09:00:00+09:00"
}
```

## 5. Google Sheets trend_history

권장 컬럼:

1. `paper_id`
2. `title`
3. `canonical_url`
4. `published_at`
5. `citation_count`
6. `topic_tag`
7. `posted_at`
8. `brief_title`

이 시트는 중복 게시 방지와 운영 추적에 사용한다.

## 6. 현재 제외 범위

현재 저장 구조에는 아래를 두지 않는다.

- 사용자 테이블
- 퀴즈 테이블
- 시도 기록
- 리더보드 캐시
- 사용자 통계 저장소
