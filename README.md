# AI 학술동아리 Discord 브리핑 자동화 저장소

이 저장소는 Google Apps Script와 Discord Webhook으로 concept 브리핑과 trend 브리핑을 자동 발행하기 위한 프로젝트다.

현재 레포의 기준은 다음과 같다.

1. 예약 실행은 Google Apps Script가 담당한다.
2. concept 브리핑은 GitHub 저장소의 markdown 원본을 읽어 게시한다.
3. trend 브리핑은 OpenAlex와 OpenAI를 사용해 생성하되, 지난 7일 논문 안에서 인용수가 높은 논문을 우선 선정한다.
4. Discord bot 명령어, 퀴즈, 리더보드, 사용자 통계 기능은 포함하지 않는다.

## 핵심 목표

1. 학술동아리 멤버가 정해진 시간에 짧고 신뢰 가능한 AI 브리핑을 받는다.
2. concept는 사람이 정리한 `.md` 원본을 기준으로 게시한다.
3. trend는 지난 7일 논문만 다루되, 그 안에서 인용수가 높은 논문을 우선 다룬다.
4. 운영자는 서버 없이도 브리핑 운영과 유지보수를 할 수 있어야 한다.

## 저장소 구조

```text
GitHub Repository
  ├─ apps-script/
  │   ├─ Code.gs
  │   ├─ ConceptService.gs
  │   ├─ TrendService.gs
  │   └─ supporting services
  ├─ content/concepts/
  │   ├─ manifest.json
  │   └─ *.md
  ├─ config/
  │   └─ trend_brief_config.json
  └─ docs/

Runtime
  ├─ Google Apps Script triggers
  ├─ Discord Webhook
  ├─ OpenAlex
  ├─ OpenAI
  ├─ Script Properties
  └─ Google Sheets history
```

## 주요 디렉터리

- `apps-script/`
  실제 운영 코드
- `content/concepts/`
  concept 브리핑 원본과 manifest
- `config/trend_brief_config.json`
  trend 수집/선정/분류 설정
- `docs/`
  구조, 설치, 운영 기준 문서

## 빠른 이해

### Concept 흐름
1. `content/concepts/manifest.json`에서 다음 항목을 찾는다.
2. 해당 markdown를 GitHub raw로 읽는다.
3. GAS가 embed를 만들어 Discord webhook으로 보낸다.
4. Script Properties에 progress를 기록한다.

### Trend 흐름
1. `config/trend_brief_config.json`을 읽는다.
2. OpenAlex에서 지난 7일 논문 후보를 수집한다.
3. 인용수 기준으로 상위 후보를 고르고 OpenAI로 브리핑을 생성한다.
4. Discord webhook으로 게시한다.
5. Google Sheets `trend_history`에 기록한다.

## 현재 trend 세부분야

- `Foundation Models(파운데이션 모델)`
- `Vision Perception(비전 인지)`
- `Multimodal Agents(멀티모달 에이전트)`
- `Speech and Audio(음성·오디오)`
- `Retrieval and Search(검색·리트리벌)`
- `Robotics and Embodied AI(로보틱스·체화 AI)`
- `Generation and Creative(생성·크리에이티브)`
- `Data and Training(데이터·학습)`
- `Systems Efficiency(시스템 효율화)`
- `Other(기타)`

## 실행 방식

로컬 Python 서버나 Discord bot 런타임은 사용하지 않는다.

운영 순서:

1. GitHub에서 content/config 수정
2. `npx clasp push`
3. GAS에서 `runConceptDaily()` 또는 `runTrendWeekly()` 실행
4. Discord 채널과 Apps Script 로그 확인

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

## 로컬 작업 명령

```bash
npm install
npx clasp login
npx clasp status
npx clasp push
npx clasp pull
npx clasp open
```

## 문서 맵

- `docs/ARCHITECTURE.md`
  시스템 구조와 데이터 흐름
- `docs/GAS_SETUP_GUIDE.md`
  최초 설치, Script Properties, 수동 검증
- `docs/OPERATIONS.md`
  운영 기본값, 로그, 재시도, 유지보수
- `docs/CONTENT_PIPELINE.md`
  브리핑 작성 기준과 품질 규칙
- `docs/DATABASE_SCHEMA.md`
  Script Properties와 Google Sheets 상태 저장 구조
- `docs/PRD.md`
  제품 범위와 목표
- `docs/ROADMAP.md`
  다음 단계 우선순위
- `docs/LINUX_OPENCODE_SETUP.md`
  OpenCode로 이 레포를 다루는 최소 가이드

## 현재 범위

- concept 브리핑 자동 게시
- trend 브리핑 자동 게시
- 게시 이력과 운영 문서 관리

## 제외 범위

- Discord interaction
- 퀴즈 제출/채점
- 리더보드
- 사용자 통계
