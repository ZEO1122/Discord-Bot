# AI 학술동아리 Discord 브리핑 자동화 저장소

이 저장소는 **딥러닝 개념 브리핑 + 최신 동향 브리핑**을 Discord로 자동 발행하기 위한 프로젝트다.

현재 운영 방식은 아래와 같다.

1. **Google Apps Script**가 예약 실행을 담당한다.
2. concept 브리핑은 GitHub public 저장소의 markdown 파일을 읽어 게시한다.
3. trend 브리핑은 GAS가 최신 source를 수집하고 GPT API로 생성한다.
4. Discord 전송은 webhook으로 처리한다.

## 핵심 목표

1. 학술동아리 멤버가 정해진 시간에 짧고 신뢰 가능한 AI 브리핑을 받는다.
2. concept는 사람이 정리한 `.md` 원본을 기반으로 게시한다.
3. trend는 최신 source를 바탕으로 생성하되, 주의 문구와 출처를 반드시 함께 보낸다.
4. 운영자는 서버 없이도 브리핑 운영/수정/유지보수를 할 수 있어야 한다.

## 현재 프로젝트 해석

이 저장소는 "상시 Discord 봇 서비스"가 아니라, 아래 경로를 기본으로 하는 **콘텐츠 저장소 + GAS 실행기 구조**다.

```text
GitHub Public Repo
  ├─ concept markdown
  ├─ concept manifest
  └─ channel interest config

Google Apps Script
  ├─ daily concept trigger
  ├─ weekly trend trigger
  ├─ GitHub raw fetch
  ├─ OpenAI generate
  ├─ Discord webhook send
  ├─ Script Properties
  └─ Google Sheets history
```

## 처음 보는 사람이 읽을 순서

1. 전체 구조 이해: `README.md`
2. 새 Discord 서버 연결: `docs/SERVER_SETUP_GUIDE.md`
3. 서버 전환 준비: `docs/CLUB_SERVER_TRANSITION.md`
4. 빠른 운영 요약: `docs/ONE_PAGE_OPERATIONS.md`
5. 운영 시작 전 최종 점검: `docs/GAS_FINAL_CHECKLIST.md`
6. Apps Script 설정: `docs/GAS_SETUP_GUIDE.md`
7. Apps Script 가져오기 순서: `docs/GAS_IMPORT_CHECKLIST.md`
8. 운영/수정/장애 대응: `docs/MAINTENANCE_GUIDE.md`, `docs/OPERATIONS.md`

## 주요 문서

- `docs/ARCHITECTURE.md`
  GAS 중심 시스템 구조
- `docs/SERVER_SETUP_GUIDE.md`
  새 Discord 서버 연결용 사용 설명서
- `docs/CLUB_SERVER_TRANSITION.md`
  개인 테스트 서버에서 동아리 서버로 전환하는 체크리스트
- `docs/ONE_PAGE_OPERATIONS.md`
  운영자용 1페이지 요약
- `docs/GAS_FINAL_CHECKLIST.md`
  실제 운영 시작 직전 확인용 최종 체크리스트
- `docs/MAINTENANCE_GUIDE.md`
  유지보수 절차
- `docs/OPERATIONS.md`
  상세 운영/장애 대응
- `docs/GAS_MIGRATION_PLAN.md`
  GAS 운영 구조 요약
- `docs/GAS_SETUP_GUIDE.md`
  Script Properties, Sheet, trigger 설정 방법
- `docs/GAS_IMPORT_CHECKLIST.md`
  Apps Script 파일을 붙여넣는 순서

## 권장 기술 스택

- 콘텐츠 저장소: GitHub public repo
- 실행기: Google Apps Script
- Discord 게시: Discord Webhook
- 동향 생성: GPT API (`gpt-5.1`)
- concept progress 저장: Script Properties
- trend history 저장: Google Sheets
- 로컬 개발/실험: Python 3.11+, SQLite

## 저장소 핵심 구조

```text
.
├─ apps-script/
├─ config/
├─ content/
├─ docs/
├─ scripts/
└─ src/
```

## 운영 원칙 요약

- trend 브리핑은 출처 없이 자동 게시하지 않는다.
- concept 브리핑은 `.md` 본문 섹션을 Discord full embed field로 전송한다.
- trend 브리핑은 아래 구조를 유지한다.
  - 주제
  - 핵심 설명
  - 왜 중요한가
  - 용어 빠르게 이해하기
  - 생각해볼 질문
  - 출처
  - 주의

## concept 원본 형식

concept 브리핑은 `frontmatter + 본문 섹션` 형식을 사용한다.

필수 frontmatter:
- `briefing_key`
- `track`
- `mode`
- `title`
- `one_line`

권장 본문 섹션:
- `정의`
- `핵심 정리`
- `왜 중요한가`
- `공부 포인트`
- `직관`
- `예시`
- `용어 빠르게 이해하기`
- `헷갈리기 쉬운 점`
- `셀프 체크`
- `토론 거리`
- `source`
- `주의`

## concept 게시 기준

- source of truth: `content/concepts/manifest.json`
- 게시 순서 상태: Script Properties
- concept는 평일 오전 9시 KST에 1개씩 게시

## trend 게시 기준

- source of truth: `config/channel_interest_map.json`
- 기본 taxonomy:
  - `llm`
  - `detection-segmentation`
  - `vision-language`
- trend history는 Google Sheets에 저장
- trend는 월요일 오전 9시 KST에 채널별로 게시

## Apps Script 전환 준비

아래 문서를 순서대로 보면 된다.

- `docs/GAS_MIGRATION_PLAN.md`
- `docs/GAS_SETUP_GUIDE.md`
- `docs/GAS_IMPORT_CHECKLIST.md`

Apps Script 코드 위치:

- `apps-script/`

## 현재 구현 상태 해석

- `apps-script/`가 현재 운영 기준 구현이다.
- `src/`와 `scripts/`는 과거 Python 구현 및 참고용이다.
- `SQLite`는 로컬 개발/실험용이다.
- Discord 자동 게시의 기준 실행기는 GAS다.
