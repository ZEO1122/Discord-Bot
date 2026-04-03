# AI 학술동아리 Discord 브리핑 자동화 저장소

이 저장소는 Google Apps Script와 Discord Webhook으로 AI 브리핑을 자동 발행하기 위한 프로젝트다.

현재 운영 기준은 다음과 같다.

1. 예약 실행은 Google Apps Script가 담당한다.
2. concept 브리핑은 GitHub 저장소의 markdown 원본을 읽어 게시한다.
3. trend 브리핑은 OpenAlex와 OpenAI를 사용해 생성한 뒤 게시한다.
4. Discord bot 명령어, 퀴즈, 리더보드, 사용자 통계 기능은 포함하지 않는다.

## 핵심 목표

1. 학술동아리 멤버가 정해진 시간에 짧고 신뢰 가능한 AI 브리핑을 받는다.
2. concept는 사람이 정리한 `.md` 원본을 기준으로 게시한다.
3. trend는 최신 논문 기반으로 생성하되, 주의 문구와 출처를 반드시 함께 보낸다.
4. 운영자는 서버 없이도 브리핑 운영과 유지보수를 할 수 있어야 한다.

## 현재 구조

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
  ├─ Discord webhook send
  ├─ Script Properties
  └─ Google Sheets history
```

## 먼저 읽을 문서

1. `README.md`
2. `docs/ARCHITECTURE.md`
3. `docs/GAS_SETUP_GUIDE.md`
4. `docs/GAS_IMPORT_CHECKLIST.md`
5. `docs/GAS_FINAL_CHECKLIST.md`
6. `docs/OPERATIONS.md`
7. `docs/MAINTENANCE_GUIDE.md`

## 주요 디렉터리

- `apps-script/`
  실제 운영 코드
- `content/concepts/`
  concept 브리핑 원본
- `config/trend_brief_config.json`
  trend 생성/선정 설정
- `docs/`
  운영 및 구조 문서

## 실행 방식

로컬 Python 서버나 Discord bot 런타임은 사용하지 않는다.

운영 흐름:

1. GitHub에서 content/config 관리
2. `clasp push`로 Apps Script 반영
3. GAS 트리거 또는 수동 실행으로 게시

## 필수 Script Properties

- `DISCORD_WEBHOOK_URL`
- `TREND_WEBHOOK_URL`
- `OPENAI_API_KEY`
- `OPENAI_MODEL`
- `GITHUB_RAW_BASE_URL`
- `CONCEPT_MANIFEST_PATH`
- `TREND_CONFIG_PATH`
- `TREND_HISTORY_SHEET_ID`
- `TREND_HISTORY_SHEET_NAME`

## 현재 범위

- concept 브리핑 자동 게시
- trend 브리핑 자동 게시
- 게시 이력과 운영 문서 관리

## 제외 범위

- Discord interaction
- 실시간 Discord 상호작용
- 퀴즈 제출/채점
- 리더보드
- 사용자 통계
