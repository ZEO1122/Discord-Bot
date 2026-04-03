# Architecture — GAS 중심 발행 구조

## 문서 목적

현재 시스템은 GitHub public repo를 콘텐츠 저장소로 쓰고, Google Apps Script를 예약 실행기로 사용한다.

## 기본 구조

```text
GitHub Public Repo
  ├─ content/concepts/*.md
  ├─ content/concepts/manifest.json
  └─ config/trend_brief_config.json

Google Apps Script
  ├─ runConceptDaily()
  ├─ runTrendWeekly()
  ├─ GitHub raw fetch
  ├─ OpenAlex fetch
  ├─ OpenAI generate
  ├─ OpenAI topic tagging
  ├─ Discord webhook send
  ├─ Script Properties
  └─ Google Sheets history
```

## Concept 브리핑 자동 게시

### 흐름
1. `manifest.json` 읽기
2. Script Properties에서 last index 읽기
3. 다음 concept 선택
4. markdown 파싱
5. embed 생성
6. concept webhook 게시
7. Script Properties progress 갱신

## Trend 브리핑 자동 게시

### 흐름
1. `trend_brief_config.json` 읽기
2. 지난 7일 논문 후보 수집
3. citation_count 기준 정렬
4. 상위 3편 선택
5. Google Sheets history 기준 중복 제거
6. few-shot topic tagging
7. GPT API 호출
8. Discord embed 생성
9. 공용 trend 채널 webhook 게시
10. Google Sheets history 기록

## 저장 전략

### Concept progress
- Script Properties

### Trend history
- Google Sheets `trend_history`
- 컬럼:
  - `paper_id`
  - `title`
  - `canonical_url`
  - `published_at`
  - `citation_count`
  - `topic_tag`
  - `posted_at`
  - `brief_title`

## 운영 기본값

- concept: 평일 오전 9시 KST
- trend: 월요일 오전 9시 KST

## Trend 선정 원칙

- 반드시 지난 7일 안에 공개된 논문만 후보로 본다.
- 같은 기간 안에서는 citation_count가 높은 논문을 우선 선택한다.

## 결론

현재 이 프로젝트는 **GAS 중심 브리핑 자동화 시스템**이다.
