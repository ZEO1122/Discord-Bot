# AI 학술동아리 Discord 브리핑 자동화 저장소

이 저장소는 **딥러닝 개념 브리핑 + 최신 동향 브리핑**을 Discord로 자동 발행하기 위한 프로젝트다.

현재 운영 기준은 다음과 같다.

1. **Google Apps Script**가 예약 실행을 담당한다.
2. concept 브리핑은 GitHub public 저장소의 markdown 파일을 읽어 게시한다.
3. trend 브리핑은 최근 7일 논문 중 인용수 높은 상위 3편을 선정하고, few-shot으로 분야 태그를 붙여 GPT API로 생성한다.
4. Discord 전송은 webhook으로 처리한다.

## 핵심 목표

1. 학술동아리 멤버가 정해진 시간에 짧고 신뢰 가능한 AI 브리핑을 받는다.
2. concept는 사람이 정리한 `.md` 원본을 기반으로 게시한다.
3. trend는 최신 논문을 바탕으로 생성하되, 주의 문구와 출처를 반드시 함께 보낸다.
4. 운영자는 서버 없이도 브리핑 운영/수정/유지보수를 할 수 있어야 한다.

## 프로젝트 해석

이 저장소는 Discord bot 서비스가 아니라, 아래 경로를 기본으로 하는 **콘텐츠 저장소 + GAS 실행기 구조**다.

```text
GitHub Public Repo
  ├─ concept markdown
  ├─ concept manifest
  └─ trend brief config

Google Apps Script
  ├─ runConceptDaily()
  ├─ runTrendWeekly()
  ├─ GitHub raw fetch
  ├─ OpenAlex fetch
  ├─ OpenAI generate
  ├─ OpenAI few-shot topic tagging
  ├─ Discord webhook send
  ├─ Script Properties
  └─ Google Sheets history
```

## 문서 읽는 순서

1. `README.md`
2. `docs/SERVER_SETUP_GUIDE.md`
3. `docs/GAS_SETUP_GUIDE.md`
4. `docs/GAS_IMPORT_CHECKLIST.md`
5. `docs/GAS_FINAL_CHECKLIST.md`
6. `docs/OPERATIONS.md`
7. `docs/MAINTENANCE_GUIDE.md`

## 주요 문서

- `docs/ARCHITECTURE.md`
- `docs/SERVER_SETUP_GUIDE.md`
- `docs/CLUB_SERVER_TRANSITION.md`
- `docs/ONE_PAGE_OPERATIONS.md`
- `docs/GAS_FINAL_CHECKLIST.md`
- `docs/MAINTENANCE_GUIDE.md`
- `docs/OPERATIONS.md`
- `docs/GAS_MIGRATION_PLAN.md`
- `docs/GAS_SETUP_GUIDE.md`
- `docs/GAS_IMPORT_CHECKLIST.md`
- `docs/LEADERBOARD_STRATEGY.md`

## 권장 기술 스택

- 콘텐츠 저장소: GitHub public repo
- 실행기: Google Apps Script
- Discord 게시: Discord Webhook
- 논문 메타데이터: OpenAlex
- 동향 생성: GPT API (`gpt-5.1`)
- concept progress 저장: Script Properties
- trend history 저장: Google Sheets

## trend 기준

- source of truth: `config/trend_brief_config.json`
- 최근 7일 논문 수집
- citation count 기준 상위 3편 선정
- few-shot taxonomy:
  - `llm`
  - `detection-segmentation`
  - `vision-language`
  - `other`
- trend history는 Google Sheets에 저장
- trend는 월요일 오전 9시 KST에 공용 trend 채널 1개로 게시

## 현재 구현 상태 해석

- `apps-script/`가 현재 운영 기준 구현이다.
- `src/`와 `scripts/`는 과거 Python 구현 및 참고용이다.
- Discord bot/interaction 기능은 제품 범위에서 제외한다.
