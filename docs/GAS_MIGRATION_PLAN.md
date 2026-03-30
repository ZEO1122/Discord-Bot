# GAS Migration Plan

## 목적

이 문서는 현재 GitHub Actions 기반 Discord 브리핑 자동화를 Google Apps Script 기반으로 전환하기 위한 계획을 정리한다.

전환 목표:
- concept 브리핑: 평일 오전 9시 KST 자동 게시
- trend 브리핑: 월요일 오전 9시 KST 채널별 자동 게시
- concept 원본: GitHub public repo markdown 파일
- trend history: Google Sheets
- concept progress: Script Properties

## 왜 전환하는가

- GitHub Actions schedule은 예약 실행 타이밍이 운영 기준으로 충분히 예측 가능하지 않았다.
- 별도 서버 없이 더 안정적인 예약 실행기가 필요하다.
- Google Apps Script는 시간 기반 트리거와 운영 UI가 단순해 현재 운영 조건에 더 적합하다.

## 유지할 것

- `content/concepts/**/*.md`
- `content/concepts/manifest.json`
- `config/channel_interest_map.json`
- Discord webhook 구조
- trend taxonomy
  - `llm`
  - `detection-segmentation`
  - `vision-language`
- 운영 문서 자산

## 단계적으로 비활성화할 것

- `.github/workflows/post-concept.yml`
- `.github/workflows/post-trend.yml`
- GitHub Actions 기반 자동 예약 발행
- Python 운영 스크립트 기반 예약 실행 경로

## 새 기본 구조

```text
GitHub Public Repo
  ├─ content/concepts/*.md
  ├─ content/concepts/manifest.json
  └─ config/channel_interest_map.json

Google Apps Script
  ├─ runConceptDaily()
  ├─ runTrendWeekly()
  ├─ GitHub raw fetch
  ├─ Discord webhook send
  ├─ OpenAI generate
  ├─ Script Properties
  └─ Google Sheets history
```

## 상태 저장 전략

### Concept progress
- 저장 위치: Script Properties
- 저장 키 예시:
  - `CONCEPT_LAST_INDEX`
  - `CONCEPT_LAST_PATH`
  - `CONCEPT_LAST_BRIEFING_KEY`
  - `CONCEPT_LAST_POSTED_AT`

### Trend history
- 저장 위치: Google Sheets
- 시트 이름: `trend_history`
- 컬럼:
  - `channel_key`
  - `channel_id`
  - `interest`
  - `source_url`
  - `source_title`
  - `published_at`
  - `posted_at`
  - `brief_title`

## 구현 순서

1. GAS 설정 문서 추가
2. Apps Script 프로젝트 스켈레톤 추가
3. concept daily 먼저 구현
4. concept 수동 테스트
5. trend weekly 구현
6. trend 채널별 수동 테스트
7. GitHub Actions 예약 비활성화
8. Apps Script time trigger 활성화

## 검증 기준

### concept
- 다음 concept 1개를 정상 게시
- Script Properties progress 증가

### trend
- 채널별 관심분야 브리핑 게시
- Google Sheets history 기록
- fresh source 없으면 skip

## Cutover 기준

아래를 모두 만족하면 GitHub Actions 자동 예약을 끄고 GAS로 전환한다.

- concept 수동 실행 성공
- trend 채널별 수동 실행 성공
- Script Properties 갱신 확인
- Google Sheets history 기록 확인
- Discord 게시 형식 확인

## 권장 운영 방침

- concept는 GitHub raw에서 읽어온다.
- trend는 Apps Script가 직접 source를 수집한다.
- GitHub는 source-of-truth 저장소로 유지한다.
- Google Apps Script는 실행기 역할만 맡긴다.
